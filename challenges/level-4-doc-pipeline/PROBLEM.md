# Level 4: Document Processing Pipeline

**Time Budget:** ~3-4 hours  
**Difficulty:** High  
**Focus:** Architecture, extensibility, NLP, full-text search, pipeline design

## Problem Statement

Design and implement a document processing pipeline that ingests files, extracts text, performs NLP analysis, indexes content for search, and exposes the results via a REST API. The architecture must support adding new processing stages without modifying existing ones.

## Requirements

### Pipeline Stages

The pipeline processes documents through a series of stages:

1. **Ingestion**: Watch a directory for new PDF and text files. Detect file type and route to appropriate extractor.

2. **Text Extraction**: Extract plain text from documents.
   - Plain text files (`.txt`, `.md`): Read directly
   - PDF files (`.pdf`): Extract text using `pypdf`, `pdfplumber`, or similar

3. **NLP Processing**: Analyze extracted text.
   - **Entity extraction**: Identify named entities (people, organizations, locations)
   - **Key phrase extraction**: Extract significant phrases and topics
   - **Summary generation**: Generate a brief summary (first N sentences or extractive summary)
   - **Word count and reading time**: Calculate document statistics

4. **Indexing**: Index processed documents for full-text search.
   - Use SQLite FTS5 or Whoosh for the search index
   - Support keyword search with relevance ranking
   - Support filtering by entity type, date range, or file type

5. **Storage**: Persist all extracted metadata in SQLite.

### REST API

```
POST   /api/documents/upload          # Upload a document for processing
GET    /api/documents                  # List all processed documents
GET    /api/documents/{id}             # Get document details + extracted metadata
DELETE /api/documents/{id}             # Remove a document

GET    /api/search?q=query             # Full-text search across documents
GET    /api/search?q=query&type=pdf    # Search with filters

GET    /api/entities                   # List all extracted entities
GET    /api/entities?type=PERSON       # Filter entities by type

GET    /api/stats                      # Pipeline statistics (docs processed, avg time, etc.)
```

### Admin CLI

```bash
# Reprocess a document
python -m doc_pipeline reprocess --id 123

# Rebuild the search index
python -m doc_pipeline reindex

# Show pipeline statistics
python -m doc_pipeline stats

# Watch a directory for new files
python -m doc_pipeline watch /path/to/incoming/
```

### Architecture Requirements

The pipeline must be designed for extensibility:

1. **Plugin Architecture**: New processing stages can be added by creating a new class that implements a `PipelineStage` interface (or similar pattern). No existing code should need modification to add a new stage.

2. **Stage Ordering**: Stages execute in a defined order. The system should support declaring stage dependencies.

3. **Error Isolation**: If one stage fails, the error should be logged but other stages should continue. Documents with failed stages should be marked appropriately.

4. **Architecture Diagram**: Include a diagram (Mermaid, ASCII art, or image) showing the pipeline flow and component relationships.

## Example NLP Output

For a document about quarterly earnings:

```json
{
  "document_id": 1,
  "filename": "q3-earnings.pdf",
  "file_type": "pdf",
  "word_count": 2450,
  "reading_time_minutes": 9.8,
  "summary": "Q3 revenue increased 12% YoY to $4.2B, driven by cloud services growth...",
  "entities": [
    {"text": "Amazon", "type": "ORGANIZATION", "count": 15},
    {"text": "Andy Jassy", "type": "PERSON", "count": 3},
    {"text": "Seattle", "type": "LOCATION", "count": 2}
  ],
  "key_phrases": [
    "cloud services growth",
    "operating margin",
    "quarterly revenue"
  ],
  "processed_at": "2026-04-01T14:30:00Z",
  "processing_time_ms": 1250
}
```

## Deliverables

1. Pipeline application with all five stages
2. REST API with all endpoints
3. Admin CLI for management operations
4. Architecture diagram
5. Comprehensive tests (unit and integration)
6. README with architecture decisions documented

## Open Decisions (Agent's Choice)

- NLP library: spaCy, NLTK, transformers, or regex-based extraction
- Search engine: SQLite FTS5, Whoosh, or other
- Web framework: FastAPI, Flask, or other
- Pipeline orchestration: custom, Celery, or async tasks
- Plugin discovery mechanism: ABC, entry points, decorators, or directory scanning
- File watching: watchdog, polling, or inotify
- How to handle large documents
- Caching strategy for NLP results

## Evaluation Criteria

See `evaluation/rubric.md` for the full scoring rubric. Key weights for this level:

- **Correctness**: 15%
- **Code Quality**: 15%
- **Architecture**: 30%
- **Testing**: 15%
- **Error Handling**: 10%
- **Documentation**: 10%
- **Bonus (Extensibility)**: 5%
