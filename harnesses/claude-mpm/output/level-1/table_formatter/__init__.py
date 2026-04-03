"""table_formatter - Convert CSV files to Markdown tables.

Public API
----------
>>> from table_formatter.formatter import read_csv, format_table
>>> from table_formatter.detector import detect_column_types
>>> headers, rows = read_csv("data.csv")
>>> alignments = detect_column_types(rows, headers)
>>> print(format_table(headers, rows, alignments))
"""

from .detector import detect_column_types
from .formatter import (
    apply_filter,
    build_separator_cell,
    cell_display_width,
    format_table,
    parse_filter_expression,
    read_csv,
    sort_rows,
    truncate_cell,
)

__all__ = [
    "detect_column_types",
    "apply_filter",
    "build_separator_cell",
    "cell_display_width",
    "format_table",
    "parse_filter_expression",
    "read_csv",
    "sort_rows",
    "truncate_cell",
]
