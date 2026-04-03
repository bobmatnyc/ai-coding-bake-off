"""Main application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from task_board.database import engine, Base
from task_board.routes import auth, users, boards, tasks, columns, activity
from task_board.websocket import router as websocket_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Team Task Board API",
    description="A complete team task management application with real-time updates",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(boards.router, prefix="/api/boards", tags=["boards"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(columns.router, prefix="/api", tags=["columns"])  # Note: columns routes already have /columns prefix
app.include_router(activity.router, prefix="/api/activity", tags=["activity"])
app.include_router(websocket_router, prefix="/ws", tags=["websocket"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Team Task Board API"}

# For running with python -m task_board
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
