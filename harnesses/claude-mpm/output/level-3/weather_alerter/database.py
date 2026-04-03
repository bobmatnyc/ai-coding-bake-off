"""SQLite database setup and schema initialization."""

import os
import sqlite3
import threading
from typing import Generator

# Thread-local storage for connections
_thread_local = threading.local()

# Module-level connection for in-memory (testing) mode
_memory_conn: sqlite3.Connection | None = None
_memory_lock = threading.Lock()


def get_db_path() -> str:
    """Get the database file path from environment."""
    return os.getenv("DATABASE_PATH", "weather.db")


def is_testing() -> bool:
    """Check if running in test mode."""
    return os.getenv("TESTING", "false").lower() == "true"


def _get_memory_connection() -> sqlite3.Connection:
    """Get or create the shared in-memory connection for testing."""
    global _memory_conn
    with _memory_lock:
        if _memory_conn is None:
            _memory_conn = sqlite3.connect(":memory:", check_same_thread=False)
            _memory_conn.row_factory = sqlite3.Row
            _memory_conn.execute("PRAGMA foreign_keys = ON")
            _create_schema(_memory_conn)
        return _memory_conn


def reset_memory_db() -> None:
    """Reset the in-memory database (for testing)."""
    global _memory_conn
    with _memory_lock:
        if _memory_conn is not None:
            _memory_conn.close()
        _memory_conn = sqlite3.connect(":memory:", check_same_thread=False)
        _memory_conn.row_factory = sqlite3.Row
        _memory_conn.execute("PRAGMA foreign_keys = ON")
        _create_schema(_memory_conn)


def get_connection() -> sqlite3.Connection:
    """Get a database connection appropriate for the current mode."""
    if is_testing():
        return _get_memory_connection()

    # Per-thread connections for production
    if not hasattr(_thread_local, "conn") or _thread_local.conn is None:
        _thread_local.conn = sqlite3.connect(
            get_db_path(), check_same_thread=False
        )
        _thread_local.conn.row_factory = sqlite3.Row
        _thread_local.conn.execute("PRAGMA foreign_keys = ON")
        # Always ensure schema exists on new connections
        _create_schema(_thread_local.conn)
    return _thread_local.conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency: yield a database connection."""
    conn = get_connection()
    try:
        yield conn
    finally:
        if not is_testing():
            conn.commit()


def _create_schema(conn: sqlite3.Connection) -> None:
    """Create all database tables."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS thresholds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
            metric TEXT NOT NULL CHECK(metric IN ('temperature','humidity','wind_speed')),
            operator TEXT NOT NULL CHECK(operator IN ('gt','lt','gte','lte')),
            value REAL NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS alert_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL REFERENCES cities(id),
            threshold_id INTEGER NOT NULL REFERENCES thresholds(id),
            triggered_at TEXT NOT NULL,
            metric_value REAL NOT NULL,
            message TEXT NOT NULL
        );
        """
    )
    conn.commit()


def init_db() -> None:
    """Initialize the database schema."""
    conn = get_connection()
    _create_schema(conn)


# Auto-initialize in-memory DB when TESTING=true at import time
# This ensures the DB is ready even when TestClient is used without lifespan context
if is_testing():
    _get_memory_connection()
