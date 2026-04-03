"""Pipeline module with abstract base class and concrete Pipeline implementation.

Provides a plugin-based document processing pipeline where stages can be
added without modifying existing code (Open/Closed principle).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DocumentContext:
    """Shared context passed between pipeline stages.

    Accumulates results as the document passes through each stage.
    Errors are recorded per-stage but do not halt processing.
    """

    path: Path
    text: str = ""
    entities: list[dict] = field(default_factory=list)
    key_phrases: list[str] = field(default_factory=list)
    summary: str = ""
    word_count: int = 0
    reading_time_minutes: float = 0.0
    errors: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class PipelineStage(ABC):
    """Abstract base class for pipeline stages.

    Implement process() to add a new stage. Register with Pipeline.add_stage().
    No existing code needs modification to add a new stage.

    Example:
        class MyStage(PipelineStage):
            @property
            def name(self) -> str:
                return "my_stage"

            def process(self, ctx: DocumentContext) -> DocumentContext:
                # Do work here
                ctx.metadata["my_result"] = "..."
                return ctx

        pipeline = Pipeline()
        pipeline.add_stage(MyStage())
        result = pipeline.process(Path("document.txt"))
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Stage name for logging and error tracking."""
        ...

    @abstractmethod
    def process(self, ctx: DocumentContext) -> DocumentContext:
        """Process the document context and return modified context.

        Args:
            ctx: The document context to process.

        Returns:
            Modified document context.
        """
        ...


class Pipeline:
    """Document processing pipeline with pluggable stages.

    Uses a chain-of-responsibility pattern where each stage processes
    the document context in order. Stage failures are isolated and
    recorded in ctx.errors without halting the pipeline.

    Example:
        # Default pipeline
        pipeline = Pipeline()
        result = pipeline.process(Path("document.txt"))

        # Custom pipeline
        pipeline = Pipeline(stages=[ExtractionStage(), NLPStage()])
        pipeline.add_stage(SentimentStage())
        result = pipeline.process(Path("document.txt"))
    """

    def __init__(self, stages: list[PipelineStage] | None = None) -> None:
        """Initialize pipeline with optional custom stages.

        Args:
            stages: List of stages to use. If None, uses default stages:
                    ExtractionStage, NLPStage, IndexingStage.
        """
        if stages is None:
            # Default stages — lazy import to avoid circular dependencies
            from doc_pipeline.stages.extraction import ExtractionStage
            from doc_pipeline.stages.nlp_stage import NLPStage
            from doc_pipeline.stages.indexing import IndexingStage

            self._stages: list[PipelineStage] = [
                ExtractionStage(),
                NLPStage(),
                IndexingStage(),
            ]
        else:
            self._stages = list(stages)

    def add_stage(self, stage: PipelineStage) -> "Pipeline":
        """Add a stage to the pipeline.

        Args:
            stage: PipelineStage instance to add.

        Returns:
            Self, for method chaining.
        """
        self._stages.append(stage)
        return self

    @property
    def stages(self) -> list[PipelineStage]:
        """Read-only view of current stages."""
        return list(self._stages)

    def process(self, path: Path) -> dict:
        """Run the document through all pipeline stages.

        Stage failures are isolated — one stage failure does not
        prevent other stages from running.

        Args:
            path: Path to the document to process.

        Returns:
            Dictionary with processing results containing:
            - text: Extracted text
            - entities: List of entity dicts
            - key_phrases: List of key phrases
            - summary: Document summary
            - word_count: Word count
            - reading_time_minutes: Estimated reading time
            - errors: Dict of stage_name -> error_message for failed stages
            - metadata: Additional metadata from stages
        """
        ctx = DocumentContext(path=Path(path))

        for stage in self._stages:
            try:
                ctx = stage.process(ctx)
            except Exception as e:
                ctx.errors[stage.name] = str(e)

        return {
            "text": ctx.text,
            "entities": ctx.entities,
            "key_phrases": ctx.key_phrases,
            "summary": ctx.summary,
            "word_count": ctx.word_count,
            "reading_time_minutes": ctx.reading_time_minutes,
            "errors": ctx.errors,
            "metadata": ctx.metadata,
        }
