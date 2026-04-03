"""CLI argument parsing for table_formatter."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="python -m table_formatter",
        description="Format a CSV file as a Markdown table.",
    )
    parser.add_argument(
        "csv_file",
        help="Path to the CSV file to format.",
    )
    parser.add_argument(
        "--sort",
        metavar="COLUMN",
        help="Sort rows by COLUMN (ascending).",
    )
    parser.add_argument(
        "--sort-desc",
        metavar="COLUMN",
        dest="sort_desc",
        help="Sort rows by COLUMN (descending).",
    )
    parser.add_argument(
        "--filter",
        metavar="EXPRESSION",
        dest="filter_expr",
        help=(
            'Filter rows by EXPRESSION (e.g. "age>30", "name=Alice", "salary>=50000").'
        ),
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write output to FILE instead of stdout.",
    )
    parser.add_argument(
        "--max-width",
        metavar="N",
        type=int,
        help="Truncate cell content to N display columns (uses … ellipsis).",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Parameters
    ----------
    argv:
        Argument list (defaults to sys.argv[1:]).
    """
    parser = build_parser()
    return parser.parse_args(argv)
