"""Task routes: /api/tasks/..."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from task_board.database import get_db
from task_board.models import Task, BoardColumn, Activity, User, Board, Priority
from task_board.deps import get_current_user
from task_board.schemas import CreateTaskRequest, UpdateTaskRequest, MoveTaskRequest
from task_board.websocket import manager

router = APIRouter()


def _task_to_dict(t: Task) -> dict:
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description or "",
        "column_id": t.column_id,
        "assignee_id": t.assignee_id,
        "priority": t.priority.value if t.priority else "medium",
        "created_by": t.created_by,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
    }


@router.post("", status_code=201)
async def create_task(
    data: CreateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task."""
    col = db.get(BoardColumn, data.column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")

    # Validate priority
    priority = Priority.medium
    if data.priority:
        try:
            priority = Priority(data.priority)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {data.priority}")

    task = Task(
        title=data.title,
        description=data.description,
        column_id=data.column_id,
        assignee_id=data.assignee_id,
        priority=priority,
        due_date=data.due_date,
        created_by=current_user.id,
    )
    db.add(task)
    db.flush()

    # Log activity
    activity = Activity(
        board_id=col.board_id,
        user_id=current_user.id,
        task_id=task.id,
        action="created",
        details={"task_title": task.title},
    )
    db.add(activity)
    db.commit()
    db.refresh(task)

    # Broadcast WebSocket event
    try:
        await manager.broadcast(col.board_id, "task_created", _task_to_dict(task))
    except Exception:
        pass

    return _task_to_dict(task)


@router.get("")
def list_tasks(
    column_id: Optional[int] = Query(None),
    assignee_id: Optional[int] = Query(None),
    board_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List tasks with optional filters."""
    query = db.query(Task)

    if column_id is not None:
        query = query.filter(Task.column_id == column_id)
    if assignee_id is not None:
        query = query.filter(Task.assignee_id == assignee_id)
    if board_id is not None:
        # Filter by board via column
        column_ids = [
            c.id for c in db.query(BoardColumn).filter(BoardColumn.board_id == board_id).all()
        ]
        query = query.filter(Task.column_id.in_(column_ids))

    tasks = query.all()
    return [_task_to_dict(t) for t in tasks]


@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a task by ID."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return _task_to_dict(task)


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    data: UpdateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_col = db.get(BoardColumn, task.column_id)
    board_id = old_col.board_id if old_col else None

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.column_id is not None:
        new_col = db.get(BoardColumn, data.column_id)
        if not new_col:
            raise HTTPException(status_code=404, detail="Column not found")
        task.column_id = data.column_id
        board_id = new_col.board_id
    if data.assignee_id is not None:
        task.assignee_id = data.assignee_id
    if data.priority is not None:
        try:
            task.priority = Priority(data.priority)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {data.priority}")
    if data.due_date is not None:
        task.due_date = data.due_date

    # Log activity
    if board_id:
        activity = Activity(
            board_id=board_id,
            user_id=current_user.id,
            task_id=task.id,
            action="updated",
            details={"task_title": task.title},
        )
        db.add(activity)

    db.commit()
    db.refresh(task)

    # Broadcast WebSocket event
    if board_id:
        try:
            await manager.broadcast(board_id, "task_updated", _task_to_dict(task))
        except Exception:
            pass

    return _task_to_dict(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task (admin only)."""
    from task_board.models import Role
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    col = db.get(BoardColumn, task.column_id)
    board_id = col.board_id if col else None

    # Log activity before deletion
    if board_id:
        activity = Activity(
            board_id=board_id,
            user_id=current_user.id,
            task_id=task.id,
            action="deleted",
            details={"task_title": task.title},
        )
        db.add(activity)

    db.delete(task)
    db.commit()

    if board_id:
        try:
            await manager.broadcast(board_id, "task_deleted", {"task_id": task_id})
        except Exception:
            pass


@router.patch("/{task_id}/move")
async def move_task(
    task_id: int,
    data: MoveTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Move a task to a different column."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_col = db.get(BoardColumn, data.column_id)
    if not new_col:
        raise HTTPException(status_code=404, detail="Column not found")

    old_column_id = task.column_id
    task.column_id = data.column_id

    # Log activity
    activity = Activity(
        board_id=new_col.board_id,
        user_id=current_user.id,
        task_id=task.id,
        action="moved",
        details={
            "task_title": task.title,
            "from_column": old_column_id,
            "to_column": data.column_id,
        },
    )
    db.add(activity)
    db.commit()
    db.refresh(task)

    try:
        await manager.broadcast(new_col.board_id, "task_moved", _task_to_dict(task))
    except Exception:
        pass

    return _task_to_dict(task)
