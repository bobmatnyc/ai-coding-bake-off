"""Pydantic models for API request/response validation."""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    """Request model for creating a document."""

    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(default="")


class DocumentResponse(BaseModel):
    """Response model for a processed document."""

    id: int
    title: str
    file_path: str
    text: str = ""
    word_count: int = 0
    summary: str = ""
    entities: list[dict] = Field(default_factory=list)
    key_phrases: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    errors: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SearchQuery(BaseModel):
    """Request model for search."""

    query: str = Field(..., min_length=1, max_length=1000, alias="query")
    q: str | None = Field(default=None, min_length=1, max_length=1000)
    limit: int = Field(default=20, ge=1, le=100)

    @property
    def search_term(self) -> str:
        """Return the search term from either 'query' or 'q' field."""
        return self.query or self.q or ""

    model_config = {"populate_by_name": True}


class SearchResultResponse(BaseModel):
    """Response model for a search result."""

    doc_id: int
    title: str
    snippet: str
    rank: float


class EntityResponse(BaseModel):
    """Response model for an entity."""

    text: str
    type: str
    count: int = 1
    doc_id: int | None = None


class StatsResponse(BaseModel):
    """Response model for pipeline statistics."""

    total_documents: int
    total_entities: int
    total_words: int
    average_word_count: float
    supported_file_types: list[str]
