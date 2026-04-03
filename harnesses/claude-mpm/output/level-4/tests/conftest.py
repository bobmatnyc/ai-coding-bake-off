"""Shared test fixtures for the document pipeline tests."""

import tempfile
from pathlib import Path

import pytest


SAMPLE_TEXT = """Acme Corporation Q3 2024 Financial Report

Acme Corporation is pleased to report strong results for the third quarter of 2024.
Revenue increased by 12% driven by cloud services growth and international expansion.

CEO Jane Mitchell commented: "We are very pleased with our momentum and growth this
quarter. Our innovation in cloud services has been outstanding."

CFO Robert Chen added that the company expects continued growth in Q4 2024.

The company operates in San Francisco, New York, and London, serving over 5,000
enterprise customers. TechGlobal Inc. partnership has been particularly successful.

Key metrics:
- Revenue: $2.4B (up 12% YoY)
- Operating profit: $480M
- Customer growth: 15% increase
- Cloud services: 35% of total revenue
"""


@pytest.fixture
def sample_txt_file(tmp_path: Path) -> Path:
    """Create a temporary .txt file for testing."""
    f = tmp_path / "sample.txt"
    f.write_text(SAMPLE_TEXT)
    return f


@pytest.fixture
def sample_md_file(tmp_path: Path) -> Path:
    """Create a temporary .md file for testing."""
    f = tmp_path / "sample.md"
    f.write_text("# Title\n\nSome **markdown** content about Acme Corporation.")
    return f


@pytest.fixture
def empty_txt_file(tmp_path: Path) -> Path:
    """Create a temporary empty .txt file."""
    f = tmp_path / "empty.txt"
    f.write_text("")
    return f


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the test suite fixtures directory."""
    return Path(__file__).parent.parent.parent.parent.parent / \
        "challenges/level-4-doc-pipeline/test_suite/fixtures"


@pytest.fixture
def search_index():
    """Create a fresh in-memory search index."""
    from doc_pipeline.search import SearchIndex
    index = SearchIndex(":memory:")
    yield index
    index.close()
