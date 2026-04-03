"""Activity routes: /api/activity/..."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from task_board.database import get_db
from task_board.models import Activity, User
from task_board.deps import get_current_user

router = APIRouter()


@router.get("")
def list_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List recent activity across all boards."""
    activities = (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "id": a.id,
            "board_id": a.board_id,
            "user_id": a.user_id,
            "task_id": a.task_id,
            "action": a.action,
            "details": a.details or {},
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in activities
    ]
