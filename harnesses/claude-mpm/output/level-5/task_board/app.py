"""FastAPI application factory."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from task_board.database import engine
from task_board.models import Base
from task_board.routes import auth, boards, columns, tasks, users, activity
from task_board.websocket import router as ws_router

# Eagerly create tables so TestClient without context manager also works
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Ensure tables exist on startup (idempotent via CREATE IF NOT EXISTS)."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Board API",
    description="Kanban-style task board with real-time WebSocket updates",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(boards.router, prefix="/api/boards", tags=["boards"])
app.include_router(columns.router, prefix="/api", tags=["columns"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(activity.router, prefix="/api/activity", tags=["activity"])
app.include_router(ws_router, tags=["websocket"])

# Serve static files if directory exists
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
