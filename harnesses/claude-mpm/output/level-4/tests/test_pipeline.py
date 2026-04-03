"""Tests for the pipeline architecture and stage implementations."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from doc_pipeline.pipeline import DocumentContext, Pipeline, PipelineStage
from doc_pipeline.stages import ExtractionStage, NLPStage, IndexingStage, SentimentStage
from doc_pipeline.search import SearchIndex


class TestDocumentContext:
    """Tests for the DocumentContext dataclass."""

    def test_create_with_path(self, tmp_path: Path) -> None:
        """Should create a DocumentContext with a path."""
        ctx = DocumentContext(path=tmp_path / "test.txt")
        assert ctx.path == tmp_path / "test.txt"
        assert ctx.text == ""
        assert ctx.entities == []
        assert ctx.key_phrases == []
        assert ctx.summary == ""
        assert ctx.word_count == 0
        assert ctx.errors == {}
        assert ctx.metadata == {}


class TestPipelineStage:
    """Tests for the PipelineStage ABC."""

    def test_is_class(self) -> None:
        """PipelineStage should be a class."""
        assert isinstance(PipelineStage, type)

    def test_cannot_instantiate_directly(self) -> None:
        """Should not be able to instantiate PipelineStage directly."""
        with pytest.raises(TypeError):
            PipelineStage()  # type: ignore

    def test_concrete_stage_implements_interface(self) -> None:
        """Concrete stages should implement the PipelineStage interface."""
        stage = ExtractionStage()
        assert isinstance(stage, PipelineStage)
        assert hasattr(stage, "name")
        assert hasattr(stage, "process")

    def test_custom_stage_can_extend(self) -> None:
        """Should be able to create custom stages."""

        class UpperCaseStage(PipelineStage):
            @property
            def name(self) -> str:
                return "uppercase"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                ctx.metadata["uppercase_length"] = len(ctx.text.upper())
                return ctx

        stage = UpperCaseStage()
        assert isinstance(stage, PipelineStage)
        assert stage.name == "uppercase"

    def test_custom_stage_processes_context(self) -> None:
        """Custom stage should modify the DocumentContext."""

        class TagStage(PipelineStage):
            @property
            def name(self) -> str:
                return "tag"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                ctx.metadata["tagged"] = True
                return ctx

        stage = TagStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = "Some text"
        result = stage.process(ctx)
        assert result.metadata["tagged"] is True


class TestPipeline:
    """Tests for the Pipeline class."""

    def test_pipeline_creates_with_defaults(self) -> None:
        """Pipeline should create with default stages."""
        pipeline = Pipeline()
        assert len(pipeline._stages) > 0

    def test_pipeline_add_stage_returns_self(self) -> None:
        """add_stage should return the pipeline for chaining."""
        pipeline = Pipeline(stages=[])

        class NoopStage(PipelineStage):
            @property
            def name(self) -> str:
                return "noop"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                return ctx

        result = pipeline.add_stage(NoopStage())
        assert result is pipeline

    def test_pipeline_processes_txt_file(self, sample_txt_file: Path) -> None:
        """Pipeline should process a .txt file and return a dict."""
        pipeline = Pipeline()
        result = pipeline.process(sample_txt_file)

        assert isinstance(result, dict)
        assert "word_count" in result or "text" in result or "entities" in result

    def test_pipeline_result_has_expected_keys(self, sample_txt_file: Path) -> None:
        """Pipeline result should contain core keys."""
        pipeline = Pipeline()
        result = pipeline.process(sample_txt_file)

        assert "word_count" in result
        assert "text" in result
        assert "entities" in result
        assert "summary" in result
        assert "key_phrases" in result

    def test_pipeline_word_count_positive(self, sample_txt_file: Path) -> None:
        """Word count should be positive for non-empty documents."""
        pipeline = Pipeline()
        result = pipeline.process(sample_txt_file)
        assert result["word_count"] > 0

    def test_pipeline_reading_time_calculated(self, sample_txt_file: Path) -> None:
        """Reading time should be calculated."""
        pipeline = Pipeline()
        result = pipeline.process(sample_txt_file)
        assert "reading_time_minutes" in result
        assert result["reading_time_minutes"] >= 0

    def test_pipeline_errors_dict_in_result(self, sample_txt_file: Path) -> None:
        """Pipeline result should contain errors dict."""
        pipeline = Pipeline()
        result = pipeline.process(sample_txt_file)
        assert "errors" in result

    def test_pipeline_isolates_stage_errors(self, tmp_path: Path) -> None:
        """A failing stage should not halt the pipeline."""

        class FailingStage(PipelineStage):
            @property
            def name(self) -> str:
                return "failing"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                raise RuntimeError("Intentional test failure")

        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Test content for error handling.")

        pipeline = Pipeline()
        pipeline.add_stage(FailingStage())
        result = pipeline.process(txt_file)

        # Pipeline should still return a result
        assert result is not None
        # Error should be recorded
        assert "failing" in result.get("errors", {})

    def test_pipeline_with_empty_stages(self, sample_txt_file: Path) -> None:
        """Pipeline with empty stages list should return basic context."""
        pipeline = Pipeline(stages=[])
        result = pipeline.process(sample_txt_file)
        assert isinstance(result, dict)

    def test_pipeline_chaining(self, tmp_path: Path) -> None:
        """Pipeline should support method chaining for adding stages."""
        tag_values: list[str] = []

        class Tag1Stage(PipelineStage):
            @property
            def name(self) -> str:
                return "tag1"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                tag_values.append("tag1")
                return ctx

        class Tag2Stage(PipelineStage):
            @property
            def name(self) -> str:
                return "tag2"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                tag_values.append("tag2")
                return ctx

        f = tmp_path / "chain.txt"
        f.write_text("chain test")

        Pipeline(stages=[]).add_stage(Tag1Stage()).add_stage(Tag2Stage()).process(f)
        assert "tag1" in tag_values
        assert "tag2" in tag_values


class TestExtractionStage:
    """Tests for ExtractionStage."""

    def test_name_is_extraction(self) -> None:
        """Stage name should be 'extraction'."""
        assert ExtractionStage().name == "extraction"

    def test_populates_text(self, sample_txt_file: Path) -> None:
        """Should populate ctx.text with file content."""
        stage = ExtractionStage()
        ctx = DocumentContext(path=sample_txt_file)
        result = stage.process(ctx)
        assert len(result.text) > 0
        assert "Acme Corporation" in result.text

    def test_populates_word_count(self, sample_txt_file: Path) -> None:
        """Should populate ctx.word_count."""
        stage = ExtractionStage()
        ctx = DocumentContext(path=sample_txt_file)
        result = stage.process(ctx)
        assert result.word_count > 0

    def test_populates_reading_time(self, sample_txt_file: Path) -> None:
        """Should populate reading_time_minutes."""
        stage = ExtractionStage()
        ctx = DocumentContext(path=sample_txt_file)
        result = stage.process(ctx)
        assert result.reading_time_minutes >= 0

    def test_adds_file_metadata(self, sample_txt_file: Path) -> None:
        """Should add file_name and file_extension to metadata."""
        stage = ExtractionStage()
        ctx = DocumentContext(path=sample_txt_file)
        result = stage.process(ctx)
        assert "file_name" in result.metadata
        assert "file_extension" in result.metadata
        assert result.metadata["file_extension"] == ".txt"


class TestNLPStage:
    """Tests for NLPStage."""

    def test_name_is_nlp(self) -> None:
        """Stage name should be 'nlp'."""
        assert NLPStage().name == "nlp"

    def test_populates_entities(self) -> None:
        """Should populate ctx.entities."""
        stage = NLPStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = "Acme Corporation CEO Jane Mitchell announced record results."
        result = stage.process(ctx)
        assert isinstance(result.entities, list)

    def test_populates_key_phrases(self) -> None:
        """Should populate ctx.key_phrases."""
        stage = NLPStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = "Cloud services revenue growth exceeded expectations."
        result = stage.process(ctx)
        assert isinstance(result.key_phrases, list)

    def test_populates_summary(self) -> None:
        """Should populate ctx.summary."""
        stage = NLPStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = (
            "Revenue increased by 12% driven by cloud services. "
            "The company reports strong growth across all regions. "
            "International expansion contributed significantly to results."
        )
        result = stage.process(ctx)
        assert isinstance(result.summary, str)

    def test_skips_empty_text(self) -> None:
        """Should skip NLP for empty text."""
        stage = NLPStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = ""
        result = stage.process(ctx)
        assert result.entities == []
        assert result.key_phrases == []


class TestIndexingStage:
    """Tests for IndexingStage."""

    def test_name_is_indexing(self) -> None:
        """Stage name should be 'indexing'."""
        assert IndexingStage().name == "indexing"

    def test_indexes_document(self, tmp_path: Path) -> None:
        """Should add document to the search index."""
        index = SearchIndex(":memory:")
        stage = IndexingStage(search_index=index)
        ctx = DocumentContext(path=tmp_path / "test.txt")
        ctx.text = "Revenue increased by 12% driven by cloud services growth."
        stage.process(ctx)

        results = index.search("cloud services")
        assert len(results) > 0
        index.close()

    def test_marks_indexed_in_metadata(self, tmp_path: Path) -> None:
        """Should mark document as indexed in metadata."""
        index = SearchIndex(":memory:")
        stage = IndexingStage(search_index=index)
        ctx = DocumentContext(path=tmp_path / "test.txt")
        ctx.text = "Some test content."
        result = stage.process(ctx)
        assert result.metadata.get("indexed") is True
        index.close()

    def test_skips_empty_text(self, tmp_path: Path) -> None:
        """Should skip indexing for empty text."""
        index = SearchIndex(":memory:")
        stage = IndexingStage(search_index=index)
        ctx = DocumentContext(path=tmp_path / "empty.txt")
        ctx.text = ""
        result = stage.process(ctx)
        assert result.metadata.get("indexed") is not True
        index.close()


class TestSentimentStage:
    """Tests for SentimentStage."""

    def test_name_is_sentiment(self) -> None:
        """Stage name should be 'sentiment'."""
        assert SentimentStage().name == "sentiment"

    def test_positive_sentiment(self) -> None:
        """Should detect positive sentiment."""
        stage = SentimentStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = "Outstanding growth and excellent profit with strong success."
        result = stage.process(ctx)
        assert result.metadata["sentiment"] == "positive"

    def test_negative_sentiment(self) -> None:
        """Should detect negative sentiment."""
        stage = SentimentStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = "Decline and loss with poor weak deficit problems failure."
        result = stage.process(ctx)
        assert result.metadata["sentiment"] == "negative"

    def test_neutral_sentiment(self) -> None:
        """Should return neutral for balanced or empty text."""
        stage = SentimentStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = ""
        result = stage.process(ctx)
        assert result.metadata["sentiment"] == "neutral"

    def test_sentiment_scores_present(self) -> None:
        """Should include sentiment_scores in metadata."""
        stage = SentimentStage()
        ctx = DocumentContext(path=Path("/tmp/test.txt"))
        ctx.text = "Growth and positive results."
        result = stage.process(ctx)
        scores = result.metadata["sentiment_scores"]
        assert "positive" in scores
        assert "negative" in scores
        assert isinstance(scores["positive"], int)
        assert isinstance(scores["negative"], int)
