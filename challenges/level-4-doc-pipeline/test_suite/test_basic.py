"""Provided test suite for Level 4: Document Processing Pipeline.

Tests the core pipeline stages and API endpoints.
Agents must pass these tests and should write additional ones.
"""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestTextExtraction:
    """Test text extraction from different file types."""

    def test_extract_text_from_txt(self) -> None:
        """Should extract text from a .txt file."""
        try:
            from doc_pipeline.extractors import extract_text
        except ImportError:
            from extractors import extract_text

        text = extract_text(FIXTURES_DIR / "sample.txt")
        assert len(text) > 100, "Extracted text should be substantial"
        assert "Acme Corporation" in text, "Should contain key content"
        assert "revenue" in text.lower(), "Should contain financial terms"

    def test_extract_text_from_pdf(self) -> None:
        """Should extract text from a .pdf file."""
        try:
            from doc_pipeline.extractors import extract_text
        except ImportError:
            from extractors import extract_text

        text = extract_text(FIXTURES_DIR / "sample.pdf")
        assert len(text) > 10, "Should extract some text from PDF"

    def test_unsupported_file_type_raises(self) -> None:
        """Should raise an error for unsupported file types."""
        try:
            from doc_pipeline.extractors import extract_text
        except ImportError:
            from extractors import extract_text

        with pytest.raises((ValueError, TypeError, NotImplementedError)):
            extract_text(Path("/tmp/test.xyz"))


class TestNLPProcessing:
    """Test NLP analysis functionality."""

    def test_entity_extraction(self) -> None:
        """Should extract named entities from text."""
        try:
            from doc_pipeline.nlp import extract_entities
        except ImportError:
            from nlp import extract_entities

        sample_text = (FIXTURES_DIR / "sample.txt").read_text()
        entities = extract_entities(sample_text)

        assert isinstance(entities, list), "Should return a list of entities"
        assert len(entities) > 0, "Should find at least one entity"

        # Check entity structure
        first = entities[0]
        if isinstance(first, dict):
            assert "text" in first or "name" in first, "Entity should have text/name"
            assert "type" in first or "label" in first, "Entity should have type/label"
        else:
            assert hasattr(first, "text") or hasattr(first, "name")

    def test_key_phrase_extraction(self) -> None:
        """Should extract key phrases from text."""
        try:
            from doc_pipeline.nlp import extract_key_phrases
        except ImportError:
            from nlp import extract_key_phrases

        sample_text = (FIXTURES_DIR / "sample.txt").read_text()
        phrases = extract_key_phrases(sample_text)

        assert isinstance(phrases, list), "Should return a list of phrases"
        assert len(phrases) > 0, "Should find at least one key phrase"

    def test_summary_generation(self) -> None:
        """Should generate a summary of the text."""
        try:
            from doc_pipeline.nlp import generate_summary
        except ImportError:
            from nlp import generate_summary

        sample_text = (FIXTURES_DIR / "sample.txt").read_text()
        summary = generate_summary(sample_text)

        assert isinstance(summary, str), "Summary should be a string"
        assert len(summary) > 20, "Summary should be non-trivial"
        assert len(summary) < len(sample_text), "Summary should be shorter than original"


class TestPipelineArchitecture:
    """Test the pipeline extensibility architecture."""

    def test_pipeline_stage_interface_exists(self) -> None:
        """A PipelineStage base class or protocol should exist."""
        try:
            from doc_pipeline.pipeline import PipelineStage
        except ImportError:
            try:
                from pipeline import PipelineStage
            except ImportError:
                pytest.skip("PipelineStage not found - agent may use different pattern")

        # Should be a class (ABC, Protocol, or regular base)
        assert isinstance(PipelineStage, type), "PipelineStage should be a class"

    def test_pipeline_processes_document(self) -> None:
        """The pipeline should process a document through all stages."""
        try:
            from doc_pipeline.pipeline import Pipeline
        except ImportError:
            try:
                from pipeline import Pipeline
            except ImportError:
                pytest.skip("Pipeline class not found")

        pipeline = Pipeline()
        result = pipeline.process(FIXTURES_DIR / "sample.txt")

        assert result is not None, "Pipeline should return a result"

        # Result should contain extracted data
        if isinstance(result, dict):
            assert "word_count" in result or "text" in result or "entities" in result, (
                "Result should contain processed data"
            )


class TestSearchIndexing:
    """Test full-text search functionality."""

    def test_index_and_search(self) -> None:
        """Should be able to index a document and search for it."""
        try:
            from doc_pipeline.search import SearchIndex
        except ImportError:
            try:
                from search import SearchIndex
            except ImportError:
                pytest.skip("SearchIndex not found")

        index = SearchIndex(":memory:" if hasattr(SearchIndex, '__init__') else None)

        # Index a document
        index.add(
            doc_id=1,
            title="Quarterly Report",
            content="Revenue increased by 12% driven by cloud services growth.",
        )

        # Search for it
        results = index.search("cloud services")

        assert len(results) > 0, "Should find the indexed document"
