"""Column routes: /api/columns/..."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from task_board.database import get_db
from task_board.models import BoardColumn, User
from task_board.deps import get_current_user
from task_board.schemas import UpdateColumnRequest, ColumnResponse

router = APIRouter()

@router.put("/{column_id}", response_model=ColumnResponse)
def update_column(
    column_id: int,
    data: UpdateColumnRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a column."""
    col = db.get(BoardColumn, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    if data.name is not None:
        col.name = data.name
    if data.position is not None:
        col.position = data.position
    db.commit()
    db.refresh(col)
    return ColumnResponse(
        id=col.id,
        board_id=col.board_id,
        name=col.name,
        position=col.position,
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
            for t in col.tasks
        ]
    )

@router.delete("/{column_id}", status_code=204)
def delete_column(
    column_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a column."""
    col = db.get(BoardColumn, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    db.delete(col)
    db.commit()
