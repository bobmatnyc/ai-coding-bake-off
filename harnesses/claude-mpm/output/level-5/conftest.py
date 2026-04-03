"""Root conftest.py - ensures clean database state for all tests."""
import os
import pytest
from pathlib import Path


@pytest.fixture(autouse=True, scope="session")
def clean_test_db():
    """Remove SQLite database file before test session to ensure clean state."""
    db_path = Path(__file__).parent / "task_board.db"
    if db_path.exists():
        db_path.unlink()
    yield
    # Clean up after session too
    if db_path.exists():
        db_path.unlink()
