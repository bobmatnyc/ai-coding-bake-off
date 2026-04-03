"""CLI entry point for task_board management commands."""
import sys


def main() -> None:
    """Main CLI dispatcher."""
    if len(sys.argv) < 2:
        print("Usage: python -m task_board [migrate|seed|run]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "migrate":
        from task_board.database import engine
        from task_board.models import Base
        Base.metadata.create_all(bind=engine)
        print("Database tables created.")

    elif command == "seed":
        from task_board.database import engine, SessionLocal
        from task_board.models import Base
        from task_board.seed import seed_db
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_db(db)
            print("Database seeded.")
        finally:
            db.close()

    elif command == "run":
        import uvicorn
        uvicorn.run("task_board.app:app", host="0.0.0.0", port=8000, reload=True)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
