"""Extraction stage: reads file content into DocumentContext."""

from doc_pipeline.extractors import extract_text
from doc_pipeline.pipeline import DocumentContext, PipelineStage


class ExtractionStage(PipelineStage):
    """Pipeline stage that extracts text from a document file.

    Reads the file at ctx.path and populates ctx.text, ctx.word_count,
    and ctx.reading_time_minutes.
    """

    @property
    def name(self) -> str:
        return "extraction"

    def process(self, ctx: DocumentContext) -> DocumentContext:
        """Extract text and compute basic metrics.

        Args:
            ctx: Document context with path set.

        Returns:
            Context with text, word_count, and reading_time_minutes populated.
        """
        ctx.text = extract_text(ctx.path)
        words = ctx.text.split()
        ctx.word_count = len(words)
        # Average adult reading speed: 200 words per minute
        ctx.reading_time_minutes = round(ctx.word_count / 200.0, 2)
        ctx.metadata["file_name"] = ctx.path.name
        ctx.metadata["file_extension"] = ctx.path.suffix.lower()
        ctx.metadata["char_count"] = len(ctx.text)
        return ctx
