"""Authentication routes: /api/auth/..."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from task_board.database import get_db
from task_board.models import User
from task_board.auth import hash_password, verify_password, create_access_token
from task_board.schemas import RegisterRequest, LoginRequest

router = APIRouter()


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        display_name=data.display_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "display_name": user.display_name}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get an access token."""
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id, user.email)
    return {"access_token": token, "token_type": "bearer"}
