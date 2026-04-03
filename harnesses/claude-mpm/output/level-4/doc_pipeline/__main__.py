"""CLI entry point for the document pipeline.

Usage:
    python -m doc_pipeline <command> [options]

Commands:
    process   Process a document file through the pipeline
    search    Search the document index
    stats     Show pipeline statistics
    reindex   Reindex all documents in the database
"""

import argparse
import json
import sys
from pathlib import Path


def cmd_process(args: argparse.Namespace) -> int:
    """Process a document file through the pipeline."""
    from doc_pipeline.pipeline import Pipeline

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        return 1

    pipeline = Pipeline()
    result = pipeline.process(path)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"File: {result.get('path', path)}")
        print(f"Words: {result.get('word_count', 0)}")
        print(f"Reading time: {result.get('reading_time_minutes', 0):.1f} min")
        print(f"Summary: {result.get('summary', '')[:200]}")
        entities = result.get("entities", [])
        if entities:
            print(f"Entities ({len(entities)}):")
            for e in entities[:10]:
                print(f"  [{e['type']}] {e['text']}")
        key_phrases = result.get("key_phrases", [])
        if key_phrases:
            print(f"Key phrases: {', '.join(key_phrases[:5])}")
        errors = result.get("errors", {})
        if errors:
            print(f"Errors: {errors}", file=sys.stderr)

    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search documents using the FTS index."""
    from doc_pipeline.stages.indexing import get_default_index

    index = get_default_index()
    results = index.search(args.query, limit=args.limit)

    if not results:
        print("No results found.")
        return 0

    for r in results:
        print(f"[{r.doc_id}] {r.title} (rank: {r.rank:.4f})")
        print(f"  {r.snippet}")
        print()

    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Show pipeline statistics."""
    from doc_pipeline.database import get_stats

    stats = get_stats()

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(f"Total documents: {stats.get('total_documents', 0)}")
        print(f"Total entities: {stats.get('total_entities', 0)}")
        avg_words = stats.get("average_word_count", 0)
        print(f"Average word count: {avg_words:.1f}")
        common_types = stats.get("common_entity_types", {})
        if common_types:
            print("Entity type distribution:")
            for etype, count in common_types.items():
                print(f"  {etype}: {count}")

    return 0


def cmd_reindex(args: argparse.Namespace) -> int:
    """Reindex all documents from the database."""
    from doc_pipeline.database import list_documents
    from doc_pipeline.stages.indexing import get_default_index

    docs = list_documents()
    index = get_default_index()
    count = 0

    for doc in docs:
        doc_id = doc.get("id")
        text = doc.get("text", "")
        path_str = doc.get("path", "")
        if doc_id and text:
            title = Path(path_str).stem.replace("_", " ").replace("-", " ").title()
            index.add(doc_id=doc_id, title=title, content=text)
            count += 1

    print(f"Reindexed {count} documents.")
    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="doc_pipeline",
        description="Document processing pipeline CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # process command
    p_process = subparsers.add_parser("process", help="Process a document file")
    p_process.add_argument("file", help="Path to the document file")
    p_process.add_argument(
        "--json", action="store_true", help="Output results as JSON"
    )

    # search command
    p_search = subparsers.add_parser("search", help="Search the document index")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument(
        "--limit", type=int, default=10, help="Maximum results (default: 10)"
    )

    # stats command
    p_stats = subparsers.add_parser("stats", help="Show pipeline statistics")
    p_stats.add_argument(
        "--json", action="store_true", help="Output stats as JSON"
    )

    # reindex command
    subparsers.add_parser("reindex", help="Reindex all documents")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    commands = {
        "process": cmd_process,
        "search": cmd_search,
        "stats": cmd_stats,
        "reindex": cmd_reindex,
    }

    handler = commands.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
