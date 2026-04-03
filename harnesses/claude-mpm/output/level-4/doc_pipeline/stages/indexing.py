"""Indexing stage: adds document to the search index."""

from doc_pipeline.pipeline import DocumentContext, PipelineStage
from doc_pipeline.search import SearchIndex

# Module-level in-memory search index (shared across pipeline runs in same process)
_default_index: SearchIndex | None = None


def get_default_index() -> SearchIndex:
    """Get the module-level default search index."""
    global _default_index
    if _default_index is None:
        _default_index = SearchIndex(":memory:")
    return _default_index


class IndexingStage(PipelineStage):
    """Pipeline stage that indexes document content for full-text search.

    Uses SearchIndex to enable fast full-text search over processed documents.
    """

    def __init__(self, search_index: SearchIndex | None = None) -> None:
        """Initialize with optional custom search index.

        Args:
            search_index: Custom SearchIndex instance. If None, uses the
                          module-level default in-memory index.
        """
        self._index = search_index

    @property
    def name(self) -> str:
        return "indexing"

    @property
    def index(self) -> SearchIndex:
        """Get the search index, using default if not set."""
        if self._index is None:
            return get_default_index()
        return self._index

    def process(self, ctx: DocumentContext) -> DocumentContext:
        """Index the document text for search.

        Args:
            ctx: Document context with text populated.

        Returns:
            Context with indexing metadata added.
        """
        if not ctx.text:
            return ctx

        # Use a hash of the file path as document ID for the search index
        doc_id = abs(hash(str(ctx.path))) % (2**31)
        title = ctx.path.stem.replace("_", " ").replace("-", " ").title()

        self.index.add(
            doc_id=doc_id,
            title=title,
            content=ctx.text,
        )

        ctx.metadata["search_doc_id"] = doc_id
        ctx.metadata["indexed"] = True

        return ctx
