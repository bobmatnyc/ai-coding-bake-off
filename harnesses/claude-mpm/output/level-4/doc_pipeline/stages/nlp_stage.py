"""NLP stage: extracts entities, key phrases, and summary."""

from doc_pipeline.nlp import extract_entities, extract_key_phrases, generate_summary
from doc_pipeline.pipeline import DocumentContext, PipelineStage


class NLPStage(PipelineStage):
    """Pipeline stage that performs NLP analysis on extracted text.

    Requires ExtractionStage to have run first (ctx.text must be populated).
    Populates ctx.entities, ctx.key_phrases, and ctx.summary.
    """

    @property
    def name(self) -> str:
        return "nlp"

    def process(self, ctx: DocumentContext) -> DocumentContext:
        """Run NLP analysis on the document text.

        Args:
            ctx: Document context with text populated.

        Returns:
            Context with entities, key_phrases, and summary populated.
        """
        if not ctx.text:
            return ctx

        ctx.entities = extract_entities(ctx.text)
        ctx.key_phrases = extract_key_phrases(ctx.text)
        ctx.summary = generate_summary(ctx.text)

        # Add NLP metadata
        ctx.metadata["entity_count"] = len(ctx.entities)
        ctx.metadata["key_phrase_count"] = len(ctx.key_phrases)
        ctx.metadata["summary_length"] = len(ctx.summary)

        return ctx
