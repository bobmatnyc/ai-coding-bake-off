"""Entry point for `python -m table_formatter`."""

from __future__ import annotations

import sys

from .cli import parse_args
from .detector import detect_column_types
from .formatter import apply_filter, format_table, read_csv, sort_rows


def main(argv: list[str] | None = None) -> int:
    """Run the table formatter CLI.

    Returns the process exit code (0 for success, non-zero for errors).
    """
    args = parse_args(argv)

    # Read CSV
    try:
        headers, rows = read_csv(args.csv_file)
    except FileNotFoundError:
        print(f"Error: File not found: {args.csv_file!r}", file=sys.stderr)
        return 1
    except PermissionError as exc:
        print(f"Error: Cannot read file: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Error reading CSV: {exc}", file=sys.stderr)
        return 1

    # Apply filter
    if args.filter_expr:
        try:
            rows = apply_filter(rows, headers, args.filter_expr)
        except ValueError as exc:
            print(f"Error in filter expression: {exc}", file=sys.stderr)
            return 1

    # Apply sorting
    if args.sort and args.sort_desc:
        print(
            "Error: --sort and --sort-desc cannot be used together.", file=sys.stderr
        )
        return 1

    if args.sort:
        try:
            rows = sort_rows(rows, headers, args.sort, descending=False)
        except ValueError as exc:
            print(f"Error sorting: {exc}", file=sys.stderr)
            return 1

    if args.sort_desc:
        try:
            rows = sort_rows(rows, headers, args.sort_desc, descending=True)
        except ValueError as exc:
            print(f"Error sorting: {exc}", file=sys.stderr)
            return 1

    # Detect column alignments
    alignments = detect_column_types(rows, headers)

    # Build table
    table = format_table(
        headers=headers,
        rows=rows,
        alignments=alignments,
        max_width=args.max_width,
    )

    # Output
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(table)
                fh.write("\n")
        except OSError as exc:
            print(f"Error writing output file: {exc}", file=sys.stderr)
            return 1
    else:
        print(table)

    return 0


if __name__ == "__main__":
    sys.exit(main())
