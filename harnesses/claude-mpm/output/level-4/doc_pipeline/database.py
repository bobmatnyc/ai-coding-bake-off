"""Database setup and management using SQLite."""

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any


DB_PATH = ":memory:"
_connection: sqlite3.Connection | None = None


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Get a database connection.

    Args:
        db_path: Path to SQLite database or ':memory:' for in-memory.

    Returns:
        SQLite connection with row_factory set.
    """
    global _connection
    if _connection is None or db_path != DB_PATH:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _init_db(conn)
        if db_path == DB_PATH:
            _connection = conn
        return conn
    return _connection


def _init_db(conn: sqlite3.Connection) -> None:
    """Initialize database schema."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL,
            text TEXT DEFAULT '',
            word_count INTEGER DEFAULT 0,
            summary TEXT DEFAULT '',
            entities TEXT DEFAULT '[]',
            key_phrases TEXT DEFAULT '[]',
            metadata TEXT DEFAULT '{}',
            errors TEXT DEFAULT '{}',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            type TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        );

        CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
        CREATE INDEX IF NOT EXISTS idx_entities_doc_id ON entities(doc_id);
    """)
    conn.commit()


def save_document(
    conn: sqlite3.Connection,
    title: str,
    file_path: str,
    result: dict[str, Any],
) -> int:
    """Save a processed document to the database.

    Args:
        conn: Database connection.
        title: Document title.
        file_path: Path to the original file.
        result: Pipeline processing result dict.

    Returns:
        ID of the inserted document.
    """
    cursor = conn.execute(
        """INSERT INTO documents
           (title, file_path, text, word_count, summary, entities, key_phrases, metadata, errors, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            title,
            file_path,
            result.get("text", ""),
            result.get("word_count", 0),
            result.get("summary", ""),
            json.dumps(result.get("entities", [])),
            json.dumps(result.get("key_phrases", [])),
            json.dumps(result.get("metadata", {})),
            json.dumps(result.get("errors", {})),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    doc_id = cursor.lastrowid or 0

    # Save entities separately for querying
    for entity in result.get("entities", []):
        conn.execute(
            "INSERT INTO entities (doc_id, text, type, count) VALUES (?, ?, ?, ?)",
            (doc_id, entity.get("text", ""), entity.get("type", ""), entity.get("count", 1)),
        )

    conn.commit()
    return doc_id


def get_document(conn: sqlite3.Connection, doc_id: int) -> dict | None:
    """Fetch a document by ID.

    Args:
        conn: Database connection.
        doc_id: Document ID.

    Returns:
        Document dict or None if not found.
    """
    row = conn.execute(
        "SELECT * FROM documents WHERE id = ?", (doc_id,)
    ).fetchone()

    if row is None:
        return None

    return _row_to_dict(row)


def list_documents(conn: sqlite3.Connection) -> list[dict]:
    """List all documents.

    Args:
        conn: Database connection.

    Returns:
        List of document dicts.
    """
    rows = conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()
    return [_row_to_dict(row) for row in rows]


def delete_document(conn: sqlite3.Connection, doc_id: int) -> bool:
    """Delete a document and its entities.

    Args:
        conn: Database connection.
        doc_id: Document ID to delete.

    Returns:
        True if deleted, False if not found.
    """
    conn.execute("DELETE FROM entities WHERE doc_id = ?", (doc_id,))
    cursor = conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    return (cursor.rowcount or 0) > 0


def get_entities(
    conn: sqlite3.Connection, entity_type: str | None = None
) -> list[dict]:
    """Get all entities, optionally filtered by type.

    Args:
        conn: Database connection.
        entity_type: Optional entity type filter (e.g., "PERSON", "ORG").

    Returns:
        List of entity dicts.
    """
    if entity_type:
        rows = conn.execute(
            "SELECT * FROM entities WHERE type = ? ORDER BY count DESC",
            (entity_type,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM entities ORDER BY count DESC"
        ).fetchall()

    return [dict(row) for row in rows]


def get_stats(conn: sqlite3.Connection) -> dict[str, Any]:
    """Get pipeline statistics.

    Args:
        conn: Database connection.

    Returns:
        Stats dict.
    """
    docs_row = conn.execute(
        "SELECT COUNT(*) as count, SUM(word_count) as total_words, AVG(word_count) as avg_words FROM documents"
    ).fetchone()

    entities_row = conn.execute(
        "SELECT COUNT(*) as count FROM entities"
    ).fetchone()

    return {
        "total_documents": docs_row["count"] if docs_row else 0,
        "total_words": docs_row["total_words"] or 0 if docs_row else 0,
        "average_word_count": docs_row["avg_words"] or 0.0 if docs_row else 0.0,
        "total_entities": entities_row["count"] if entities_row else 0,
        "supported_file_types": [".txt", ".md", ".pdf"],
    }


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a database row to a dict with JSON fields parsed."""
    d = dict(row)
    for json_field in ("entities", "key_phrases", "metadata", "errors"):
        if json_field in d and isinstance(d[json_field], str):
            try:
                d[json_field] = json.loads(d[json_field])
            except (json.JSONDecodeError, TypeError):
                d[json_field] = [] if json_field in ("entities", "key_phrases") else {}
    return d
