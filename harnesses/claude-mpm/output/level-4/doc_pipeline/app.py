"""FastAPI application for the document processing pipeline."""

import os
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware

from doc_pipeline.database import (
    get_connection,
    save_document,
    get_document,
    list_documents,
    delete_document,
    get_entities,
    get_stats,
)
from doc_pipeline.models import (
    DocumentResponse,
    SearchQuery,
    SearchResultResponse,
    EntityResponse,
    StatsResponse,
)
from doc_pipeline.pipeline import Pipeline
from doc_pipeline.search import SearchIndex


# Module-level search index for the API
_search_index: SearchIndex | None = None


def get_search_index() -> SearchIndex:
    """Get the module-level search index for the API."""
    global _search_index
    if _search_index is None:
        _search_index = SearchIndex(":memory:")
    return _search_index


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: initialize and teardown resources."""
    # Initialize database
    conn = get_connection()
    conn.close()
    yield
    # Cleanup
    if _search_index is not None:
        _search_index.close()


app = FastAPI(
    title="Document Pipeline API",
    description="Process, search, and analyze documents via a pipeline architecture.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/documents/", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
    """Upload and process a document.

    Accepts .txt, .md, or .pdf files. Runs the full pipeline
    (extraction, NLP, indexing) and stores the result.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".txt", ".md", ".pdf"}:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {suffix}. Supported: .txt, .md, .pdf",
        )

    # Write to temp file, process, then clean up
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        from doc_pipeline.stages.indexing import IndexingStage
        from doc_pipeline.stages.extraction import ExtractionStage
        from doc_pipeline.stages.nlp_stage import NLPStage

        # Build pipeline with the API's shared search index
        pipeline = Pipeline(stages=[
            ExtractionStage(),
            NLPStage(),
            IndexingStage(get_search_index()),
        ])

        result = pipeline.process(tmp_path)

        # Build title from filename
        title = Path(file.filename).stem.replace("_", " ").replace("-", " ").title()

        # Save to database
        conn = get_connection()
        doc_id = save_document(conn, title=title, file_path=file.filename, result=result)

        # Fetch and return the saved document
        doc = get_document(conn, doc_id)
        if doc is None:
            raise HTTPException(status_code=500, detail="Failed to save document")
        return doc

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.get("/documents/", response_model=list[DocumentResponse])
async def list_docs(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
) -> list[dict[str, Any]]:
    """List all processed documents."""
    conn = get_connection()
    docs = list_documents(conn)
    return docs[offset:offset + limit]


@app.get("/documents/{doc_id}", response_model=DocumentResponse)
async def get_doc(doc_id: int) -> dict[str, Any]:
    """Get a specific document by ID."""
    conn = get_connection()
    doc = get_document(conn, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    return doc


@app.delete("/documents/{doc_id}")
async def delete_doc(doc_id: int) -> dict[str, str]:
    """Delete a document by ID."""
    conn = get_connection()
    doc = get_document(conn, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    delete_document(conn, doc_id)
    return {"message": f"Document {doc_id} deleted"}


@app.post("/search/", response_model=list[SearchResultResponse])
async def search_documents(query: SearchQuery) -> list[dict[str, Any]]:
    """Search documents using full-text search."""
    index = get_search_index()
    search_term = query.query or query.q or ""
    results = index.search(search_term, limit=query.limit)
    return [
        {
            "doc_id": r.doc_id,
            "title": r.title,
            "snippet": r.snippet,
            "rank": r.rank,
        }
        for r in results
    ]


@app.get("/search/", response_model=list[SearchResultResponse])
async def search_documents_get(
    q: str = Query(..., description="Search query"),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, Any]]:
    """Search documents using full-text search (GET endpoint)."""
    index = get_search_index()
    results = index.search(q, limit=limit)
    return [
        {
            "doc_id": r.doc_id,
            "title": r.title,
            "snippet": r.snippet,
            "rank": r.rank,
        }
        for r in results
    ]


@app.get("/documents/{doc_id}/entities", response_model=list[EntityResponse])
async def get_doc_entities(doc_id: int) -> list[dict[str, Any]]:
    """Get entities extracted from a specific document."""
    conn = get_connection()
    doc = get_document(conn, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    entities = get_entities(conn, entity_type=None)
    # Filter to this document's entities
    doc_entities = [e for e in entities if e.get("doc_id") == doc_id]
    return doc_entities


@app.get("/stats/", response_model=StatsResponse)
async def get_pipeline_stats() -> dict[str, Any]:
    """Get pipeline statistics."""
    conn = get_connection()
    return get_stats(conn)
