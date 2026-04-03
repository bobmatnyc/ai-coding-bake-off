"""Pydantic request/response schemas."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# Auth schemas
class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    display_name: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Board schemas
class CreateBoardRequest(BaseModel):
    name: str
    description: str = ""


class UpdateBoardRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    column_id: int
    assignee_id: Optional[int] = None
    priority: str
    created_by: int
    created_at: datetime
    updated_at: datetime


class ColumnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    name: str
    position: int
    tasks: List[TaskResponse] = []


class BoardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    created_by: int
    created_at: datetime
    columns: List[ColumnResponse] = []


class BoardListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    created_by: int
    created_at: datetime


# Column schemas
class CreateColumnRequest(BaseModel):
    name: str
    position: int = 0


class UpdateColumnRequest(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None


# Task schemas
class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""
    column_id: int
    assignee_id: Optional[int] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[int] = None
    assignee_id: Optional[int] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class MoveTaskRequest(BaseModel):
    column_id: int


# Activity schemas
class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    user_id: int
    task_id: Optional[int] = None
    action: str
    details: Dict[str, Any]
    created_at: datetime
```

harnesses/claude-mpm/output/level-5/task_board/routes/users.py
