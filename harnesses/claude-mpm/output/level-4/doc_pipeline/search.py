"""Search module providing full-text search via SQLite FTS5."""

import sqlite3
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result."""

    doc_id: int
    title: str
    snippet: str
    rank: float


class SearchIndex:
    """Full-text search index using SQLite FTS5.

    Provides add/search operations over document content.
    Supports in-memory and file-based storage.

    Example:
        index = SearchIndex(":memory:")
        index.add(doc_id=1, title="Q3 Report", content="Revenue increased...")
        results = index.search("revenue cloud")
        for r in results:
            print(r.title, r.snippet)
    """

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize the search index.

        Args:
            db_path: Path to SQLite database file, or ":memory:" for
                     in-memory storage. Defaults to ":memory:".
        """
        self._path = db_path if db_path is not None else ":memory:"
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        """Create FTS5 virtual table if it doesn't exist."""
        self._conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_docs
            USING fts5(title, content, doc_id UNINDEXED)
        """)
        self._conn.commit()

    def add(self, doc_id: int, title: str, content: str) -> None:
        """Add a document to the search index.

        Args:
            doc_id: Unique integer identifier for the document.
            title: Document title for display in results.
            content: Full document text to index.
        """
        self._conn.execute(
            "INSERT INTO fts_docs(doc_id, title, content) VALUES (?, ?, ?)",
            (doc_id, title, content),
        )
        self._conn.commit()

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        """Search documents using full-text search.

        Args:
            query: Search query string. Supports FTS5 query syntax.
            limit: Maximum number of results to return.

        Returns:
            List of SearchResult objects ordered by relevance.
        """
        if not query or not query.strip():
            return []

        try:
            rows = self._conn.execute(
                "SELECT doc_id, title, snippet(fts_docs, 1, '<b>', '</b>', '...', 32), rank "
                "FROM fts_docs WHERE fts_docs MATCH ? ORDER BY rank LIMIT ?",
                (query, limit),
            ).fetchall()
            return [SearchResult(r[0], r[1], r[2], r[3]) for r in rows]
        except sqlite3.OperationalError:
            # Handle malformed queries gracefully
            return []

    def remove(self, doc_id: int) -> None:
        """Remove a document from the search index.

        Args:
            doc_id: ID of the document to remove.
        """
        self._conn.execute(
            "DELETE FROM fts_docs WHERE doc_id = ?", (doc_id,)
        )
        self._conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __enter__(self) -> "SearchIndex":
        return self

    def __exit__(self, *_args: object) -> None:  # noqa: PYI036
        self.close()
