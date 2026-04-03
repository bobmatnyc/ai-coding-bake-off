# Document Processing Pipeline

A clean, extensible document processing pipeline built with Python 3.12+.

## Features

- **Multi-format extraction**: .txt, .md, .pdf support
- **Regex-based NLP**: Entity extraction (ORG, PERSON, LOCATION), key phrase extraction, extractive summarization
- **Full-text search**: SQLite FTS5 with BM25 ranking and snippet highlighting
- **Plugin architecture**: Add new stages without modifying existing code
- **REST API**: FastAPI endpoints for document upload, search, and management
- **CLI**: Command-line interface for batch processing

## Quick Start

### Installation

```bash
pip install -e ".[dev]"
```

### Run the API server

```bash
uvicorn doc_pipeline.app:app --reload
```

### Process a document via CLI

```bash
python -m doc_pipeline process path/to/document.txt
python -m doc_pipeline process path/to/report.pdf --json
```

### Search documents

```bash
python -m doc_pipeline search "cloud services revenue"
```

### View statistics

```bash
python -m doc_pipeline stats
```

## Usage

### Python API

```python
from pathlib import Path
from doc_pipeline.pipeline import Pipeline

# Process with default stages (extraction, NLP, indexing)
pipeline = Pipeline()
result = pipeline.process(Path("report.txt"))

print(result["word_count"])        # e.g. 450
print(result["summary"])           # extractive summary
print(result["entities"])          # [{"text": "Acme Corp", "type": "ORG"}, ...]
print(result["key_phrases"])       # ["cloud services", "revenue growth", ...]
print(result["reading_time_minutes"])  # e.g. 2.25
```

### Adding Custom Stages

```python
from doc_pipeline.pipeline import DocumentContext, Pipeline, PipelineStage

class ReadabilityStage(PipelineStage):
    @property
    def name(self) -> str:
        return "readability"

    def process(self, ctx: DocumentContext) -> DocumentContext:
        sentences = ctx.text.count('.') + ctx.text.count('?') + ctx.text.count('!')
        if sentences > 0 and ctx.word_count > 0:
            score = 206.835 - 1.015 * (ctx.word_count / sentences)
            ctx.metadata["readability_score"] = round(score, 2)
        return ctx

pipeline = Pipeline()
pipeline.add_stage(ReadabilityStage())
result = pipeline.process(Path("document.txt"))
print(result["metadata"]["readability_score"])
```

### Search Index

```python
from doc_pipeline.search import SearchIndex

with SearchIndex(":memory:") as index:
    index.add(doc_id=1, title="Q3 Report", content="Revenue increased by 12%...")
    results = index.search("revenue growth")
    for r in results:
        print(f"[{r.doc_id}] {r.title}: {r.snippet}")
```

### Individual NLP Functions

```python
from doc_pipeline.nlp import extract_entities, extract_key_phrases, generate_summary

text = "Acme Corporation CEO Jane Mitchell announced record Q3 results..."

entities = extract_entities(text)
# [{"text": "Acme Corporation", "type": "ORG"}, {"text": "Jane Mitchell", "type": "PERSON"}, ...]

phrases = extract_key_phrases(text)
# ["record Q3 results", "Acme Corporation", ...]

summary = generate_summary(text)
# "Acme Corporation CEO Jane Mitchell announced record Q3 results..."
```

## REST API

### Upload a document

```bash
curl -X POST http://localhost:8000/documents/ \
  -F "file=@report.txt"
```

### List documents

```bash
curl http://localhost:8000/documents/
```

### Search

```bash
curl "http://localhost:8000/search/?q=cloud+services"
```

### Get statistics

```bash
curl http://localhost:8000/stats/
```

## Docker

```bash
# Build and run
docker-compose up api

# Run tests
docker-compose run test
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=doc_pipeline --cov-report=html

# Provided benchmark tests
pytest /path/to/test_suite/test_basic.py -v
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full architecture documentation
including Mermaid diagrams and design decision rationale.

## Project Structure

```
doc_pipeline/
├── __init__.py          # Package init
├── __main__.py          # CLI entry point
├── app.py               # FastAPI application
├── pipeline.py          # Pipeline + PipelineStage ABC + DocumentContext
├── extractors.py        # Text extraction (.txt, .md, .pdf)
├── nlp.py               # NLP: entities, key phrases, summary
├── search.py            # SearchIndex with SQLite FTS5
├── database.py          # SQLite document persistence
├── models.py            # Pydantic v2 models for API
├── stages/
│   ├── __init__.py
│   ├── extraction.py    # ExtractionStage
│   ├── nlp_stage.py     # NLPStage
│   ├── indexing.py      # IndexingStage
│   └── sentiment.py     # SentimentStage (bonus)
└── routes/
    └── __init__.py
tests/
├── conftest.py
├── test_extractors.py
├── test_nlp.py
├── test_pipeline.py
├── test_search.py
└── test_api.py
```
