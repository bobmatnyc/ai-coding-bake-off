"""User routes: /api/users/..."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from task_board.database import get_db
from task_board.models import User, Role
from task_board.deps import get_current_user
from task_board.schemas import UserResponse

router = APIRouter()


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "role": current_user.role.value if current_user.role else "member",
    }


@router.get("")
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all users (admin only)."""
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "display_name": u.display_name,
            "role": u.role.value if u.role else "member",
        }
        for u in users
    ]
