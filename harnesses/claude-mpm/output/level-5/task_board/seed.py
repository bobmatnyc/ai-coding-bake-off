"""Seed data for the task board application."""
from sqlalchemy.orm import Session
from task_board.models import User, Board, BoardColumn, Task, Role, Priority
from task_board.auth import hash_password


def seed_database(db: Session) -> None:
    """Seed the database with initial data."""
    # Create admin user
    admin = User(
        email="admin@example.com",
        password_hash=hash_password("Admin123!"),
        display_name="Admin User",
        role=Role.admin,
    )
    db.add(admin)
    db.flush()

    # Create sample board
    board = Board(
        name="Sample Project",
        description="A sample project board",
        created_by=admin.id,
    )
    db.add(board)
    db.flush()

    # Create default columns
    columns = [
        BoardColumn(board_id=board.id, name="To Do", position=0),
        BoardColumn(board_id=board.id, name="In Progress", position=1),
        BoardColumn(board_id=board.id, name="Done", position=2),
    ]
    for col in columns:
        db.add(col)
    db.flush()

    # Create sample tasks
    task1 = Task(
        title="Set up project",
        description="Initialize the project repository",
        column_id=columns[2].id,
        priority=Priority.high,
        created_by=admin.id,
    )
    task2 = Task(
        title="Design API",
        description="Design the REST API endpoints",
        column_id=columns[1].id,
        priority=Priority.medium,
        created_by=admin.id,
    )
    task3 = Task(
        title="Write tests",
        description="Write unit and integration tests",
        column_id=columns[0].id,
        priority=Priority.medium,
        created_by=admin.id,
    )
    for task in [task1, task2, task3]:
        db.add(task)

    db.commit()
    print("Database seeded successfully!")
