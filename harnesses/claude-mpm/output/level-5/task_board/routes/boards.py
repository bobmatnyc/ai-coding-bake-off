"""Board routes: /api/boards/..."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from task_board.database import get_db
from task_board.models import Board, BoardColumn, Activity, User, Role
from task_board.deps import get_current_user
from task_board.schemas import (
    CreateBoardRequest,
    UpdateBoardRequest,
    CreateColumnRequest,
    BoardResponse,
    BoardListResponse,
    ColumnResponse,
    ActivityResponse,
)

router = APIRouter()

def _board_to_dict(board: Board) -> dict:
    return {
        "id": board.id,
        "name": board.name,
        "description": board.description or "",
        "created_by": board.created_by,
        "created_at": board.created_at.isoformat() if board.created_at else None,
        "columns": [_column_to_dict(c) for c in board.columns],
    }

def _column_to_dict(col: BoardColumn) -> dict:
    return {
        "id": col.id,
        "board_id": col.board_id,
        "name": col.name,
        "position": col.position,
        "tasks": [
            {
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
            for t in col.tasks
        ],
    }

@router.post("", status_code=201)
def create_board(
    data: CreateBoardRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new board with default columns."""
    board = Board(
        name=data.name,
        description=data.description,
        created_by=current_user.id,
    )
    db.add(board)
    db.flush()

    # Create default columns
    default_cols = [
        BoardColumn(board_id=board.id, name="To Do", position=0),
        BoardColumn(board_id=board.id, name="In Progress", position=1),
        BoardColumn(board_id=board.id, name="Done", position=2),
    ]
    for col in default_cols:
        db.add(col)

    # Log activity
    activity = Activity(
        board_id=board.id,
        user_id=current_user.id,
        action="created",
        details=json.dumps({"board_name": board.name}),
    )
    db.add(activity)

    db.commit()
    db.refresh(board)

    return {
        "id": board.id,
        "name": board.name,
        "description": board.description or "",
        "created_by": board.created_by,
        "created_at": board.created_at.isoformat() if board.created_at else None,
    }

@router.get("", response_model=List[BoardListResponse])
def list_boards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all boards."""
    boards = db.query(Board).all()
    return [
        BoardListResponse(
            id=b.id,
            name=b.name,
            description=b.description or "",
            created_by=b.created_by,
            created_at=b.created_at,
        )
        for b in boards
    ]

@router.get("/{board_id}", response_model=BoardResponse)
def get_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get board with columns and tasks."""
    board = db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return BoardResponse(
        id=board.id,
        name=board.name,
        description=board.description or "",
        created_by=board.created_by,
        created_at=board.created_at,
        columns=[
            ColumnResponse(
                id=c.id,
                board_id=c.board_id,
                name=c.name,
                position=c.position,
                tasks=[
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description or "",
                        "column_id": t.column_id,
                        "assignee_id": t.assignee_id,
                        "priority": t.priority.value if t.priority else "medium",
                        "created_by": t.created_by,
                        "created_at": t.created_at,
                        "updated_at": t.updated_at,
                    }
                    for t in c.tasks
                ]
            )
            for c in board.columns
        ]
    )

@router.put("/{board_id}", response_model=BoardListResponse)
def update_board(
    board_id: int,
    data: UpdateBoardRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a board."""
    board = db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if data.name is not None:
        board.name = data.name
    if data.description is not None:
        board.description = data.description
    db.commit()
    db.refresh(board)
    return BoardListResponse(
        id=board.id,
        name=board.name,
        description=board.description or "",
        created_by=board.created_by,
        created_at=board.created_at,
    )

@router.delete("/{board_id}", status_code=204)
def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a board (admin only)."""
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    board = db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()

@router.post("/{board_id}/columns", status_code=201)
def add_column(
    board_id: int,
    data: CreateColumnRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a column to a board."""
    board = db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    col = BoardColumn(board_id=board_id, name=data.name, position=data.position)
    db.add(col)
    db.commit()
    db.refresh(col)
    return {
        "id": col.id,
        "board_id": col.board_id,
        "name": col.name,
        "position": col.position,
    }

@router.get("/{board_id}/activity", response_model=List[ActivityResponse])
def get_board_activity(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get activity for a board."""
    board = db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    activities = (
        db.query(Activity)
        .filter(Activity.board_id == board_id)
        .order_by(Activity.created_at.desc())
        .limit(100)
        .all()
    )
    return [
        ActivityResponse(
            id=a.id,
            board_id=a.board_id,
            user_id=a.user_id,
            task_id=a.task_id,
            action=a.action,
            details=json.loads(a.details) if a.details else {},
            created_at=a.created_at,
        )
        for a in activities
    ]
