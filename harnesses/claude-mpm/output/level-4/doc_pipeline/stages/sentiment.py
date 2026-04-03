"""Sentiment stage: simple positive/negative sentiment analysis.

Demonstrates adding a new stage without modifying existing code.
This is a bonus/demo stage showing the plugin architecture.
"""

from doc_pipeline.pipeline import DocumentContext, PipelineStage


class SentimentStage(PipelineStage):
    """Example plugin stage: simple sentiment analysis.

    Demonstrates adding a new stage without modifying existing code.
    Add to pipeline: pipeline.add_stage(SentimentStage())

    Uses simple word-counting approach without external dependencies.
    """

    POSITIVE_WORDS = frozenset({
        "growth", "increase", "increased", "strong", "pleased", "momentum",
        "innovation", "improved", "improvement", "excellent", "outstanding",
        "success", "successful", "profit", "gain", "positive", "great",
        "good", "best", "leading", "expand", "expansion", "record",
        "breakthrough", "accelerate", "accelerating", "advance", "advancing",
    })

    NEGATIVE_WORDS = frozenset({
        "decline", "loss", "decrease", "decreased", "concern", "risk",
        "weak", "poor", "bad", "worse", "worst", "fall", "falling",
        "drop", "dropped", "challenge", "difficult", "difficult", "downturn",
        "deficit", "shortfall", "delay", "delays", "problem", "problems",
        "issue", "issues", "fail", "failure", "failed",
    })

    @property
    def name(self) -> str:
        return "sentiment"

    def process(self, ctx: DocumentContext) -> DocumentContext:
        """Analyze document sentiment and add to metadata.

        Args:
            ctx: Document context with text populated.

        Returns:
            Context with sentiment metadata added.
        """
        if not ctx.text:
            ctx.metadata["sentiment"] = "neutral"
            ctx.metadata["sentiment_scores"] = {"positive": 0, "negative": 0}
            return ctx

        words = ctx.text.lower().split()
        cleaned = [w.strip(".,!?;:\"'()[]{}") for w in words]

        pos = sum(1 for w in cleaned if w in self.POSITIVE_WORDS)
        neg = sum(1 for w in cleaned if w in self.NEGATIVE_WORDS)

        if pos > neg:
            sentiment = "positive"
        elif neg > pos:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        ctx.metadata["sentiment"] = sentiment
        ctx.metadata["sentiment_scores"] = {"positive": pos, "negative": neg}

        return ctx
