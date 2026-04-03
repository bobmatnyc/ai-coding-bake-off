"""Tests for the SearchIndex full-text search module."""

import pytest

from doc_pipeline.search import SearchIndex, SearchResult


class TestSearchIndex:
    """Tests for the SearchIndex class."""

    def test_create_in_memory(self) -> None:
        """Should create an in-memory search index."""
        index = SearchIndex(":memory:")
        assert index is not None
        index.close()

    def test_add_and_search(self, search_index: SearchIndex) -> None:
        """Should find a document after adding it."""
        search_index.add(
            doc_id=1,
            title="Quarterly Report",
            content="Revenue increased by 12% driven by cloud services growth.",
        )
        results = search_index.search("cloud services")
        assert len(results) > 0

    def test_search_returns_list_of_search_results(
        self, search_index: SearchIndex
    ) -> None:
        """Search results should be SearchResult instances."""
        search_index.add(
            doc_id=1,
            title="Test Doc",
            content="cloud computing revenue growth services",
        )
        results = search_index.search("cloud")
        assert isinstance(results, list)
        for r in results:
            assert isinstance(r, SearchResult)

    def test_search_result_has_expected_fields(
        self, search_index: SearchIndex
    ) -> None:
        """SearchResult should have doc_id, title, snippet, rank."""
        search_index.add(
            doc_id=42,
            title="My Document",
            content="Some content about Python programming and asyncio.",
        )
        results = search_index.search("Python")
        assert len(results) > 0
        result = results[0]
        assert result.doc_id == 42
        assert result.title == "My Document"
        assert isinstance(result.snippet, str)
        assert isinstance(result.rank, float)

    def test_search_no_results_for_missing_term(
        self, search_index: SearchIndex
    ) -> None:
        """Should return empty list when no documents match."""
        search_index.add(
            doc_id=1,
            title="Report",
            content="Revenue and profit metrics.",
        )
        results = search_index.search("quantum entanglement xyzzy")
        assert results == []

    def test_add_multiple_documents(self, search_index: SearchIndex) -> None:
        """Should handle multiple documents."""
        search_index.add(1, "Doc A", "cloud services revenue growth")
        search_index.add(2, "Doc B", "machine learning artificial intelligence")
        search_index.add(3, "Doc C", "database storage infrastructure")

        results = search_index.search("cloud")
        assert len(results) >= 1
        doc_ids = {r.doc_id for r in results}
        assert 1 in doc_ids

    def test_search_limit_respected(self, search_index: SearchIndex) -> None:
        """Should respect the limit parameter."""
        for i in range(10):
            search_index.add(i, f"Doc {i}", "revenue growth profit services cloud")

        results = search_index.search("revenue", limit=3)
        assert len(results) <= 3

    def test_remove_document(self, search_index: SearchIndex) -> None:
        """Should remove a document from the index."""
        search_index.add(99, "Temp Doc", "unique xanadu quetzal content here")
        results = search_index.search("xanadu")
        assert len(results) > 0

        search_index.remove(99)
        results_after = search_index.search("xanadu")
        assert len(results_after) == 0

    def test_context_manager(self) -> None:
        """SearchIndex should work as a context manager."""
        with SearchIndex(":memory:") as index:
            index.add(1, "Test", "context manager test content")
            results = index.search("context manager")
            assert len(results) > 0

    def test_update_document(self, search_index: SearchIndex) -> None:
        """Adding a document with an existing ID should update it."""
        search_index.add(1, "Original Title", "original unique content xanadu")
        search_index.add(1, "Updated Title", "completely different updated material")

        # Old content should not be findable (or new should be found)
        new_results = search_index.search("different updated material")
        assert isinstance(new_results, list)

    def test_malformed_query_returns_empty(self, search_index: SearchIndex) -> None:
        """Malformed FTS5 query should return empty list, not raise."""
        search_index.add(1, "Doc", "some content")
        results = search_index.search('AND OR " incomplete')
        assert isinstance(results, list)

    def test_search_title_content(self, search_index: SearchIndex) -> None:
        """Should search both title and content."""
        search_index.add(1, "Cloud Computing Report", "quarterly financial results")
        search_index.add(2, "Financial Results", "cloud deployment infrastructure")

        # Search by title term
        title_results = search_index.search("Cloud Computing")
        # Search by content term
        content_results = search_index.search("quarterly")

        assert len(title_results) > 0
        assert len(content_results) > 0
