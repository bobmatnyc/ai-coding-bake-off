"""Tests for the FastAPI application endpoints."""

from pathlib import Path

import pytest

try:
    from fastapi.testclient import TestClient
    from doc_pipeline.app import app

    client = TestClient(app)
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not FASTAPI_AVAILABLE, reason="FastAPI not available"
)

SAMPLE_CONTENT = b"Acme Corporation Q3 2024 Report. Revenue increased by 12% driven by cloud services growth."


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_ok(self) -> None:
        """GET /health should return 200 with status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestDocumentEndpoints:
    """Tests for document upload and management endpoints."""

    def test_upload_txt_file(self) -> None:
        """Should accept and process .txt file uploads."""
        response = client.post(
            "/documents/",
            files={"file": ("test.txt", SAMPLE_CONTENT, "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "word_count" in data or "text" in data

    def test_upload_unsupported_type_returns_415(self) -> None:
        """Should return 415 for unsupported file types."""
        response = client.post(
            "/documents/",
            files={"file": ("test.xyz", b"some content", "application/octet-stream")},
        )
        assert response.status_code == 415

    def test_list_documents(self) -> None:
        """GET /documents/ should return a list."""
        response = client.get("/documents/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_nonexistent_document_returns_404(self) -> None:
        """GET /documents/99999 should return 404."""
        response = client.get("/documents/99999")
        assert response.status_code == 404


class TestSearchEndpoints:
    """Tests for search endpoints."""

    def test_search_get_endpoint(self) -> None:
        """GET /search/ should accept a query parameter."""
        response = client.get("/search/", params={"q": "cloud services"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_search_post_endpoint(self) -> None:
        """POST /search/ should accept a JSON body."""
        response = client.post(
            "/search/",
            json={"query": "revenue growth", "limit": 5},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestStatsEndpoint:
    """Tests for the stats endpoint."""

    def test_stats_returns_dict(self) -> None:
        """GET /stats/ should return a dictionary."""
        response = client.get("/stats/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "total_documents" in data
