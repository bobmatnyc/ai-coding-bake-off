"""Column type detection for table_formatter.

Detects whether a column is numeric (for right-alignment) or text (for left-alignment).
"""

from __future__ import annotations


def is_numeric_value(value: str) -> bool:
    """Return True if the string represents a pure numeric value.

    Leading zeros disqualify a value (e.g. "01234" is not numeric).
    Empty strings are not counted as numeric.
    """
    if not value:
        return False
    # Leading zero check: "0" is fine, "01" is not
    stripped = value.strip()
    if not stripped:
        return False
    # Reject leading zeros (e.g. zip codes)
    if len(stripped) > 1 and stripped[0] == "0" and stripped[1].isdigit():
        return False
    # Try to parse as float
    try:
        float(stripped)
        return True
    except ValueError:
        return False


def detect_column_types(rows: list[list[str]], headers: list[str]) -> list[str]:
    """Detect alignment for each column.

    Returns a list of alignment strings, one per column:
    - "right"  for numeric columns (all non-empty values parseable as float, no leading zeros)
    - "left"   otherwise
    """
    num_cols = len(headers)
    alignments: list[str] = []

    for col_idx in range(num_cols):
        non_empty_values = [
            row[col_idx]
            for row in rows
            if col_idx < len(row) and row[col_idx].strip()
        ]

        if non_empty_values and all(is_numeric_value(v) for v in non_empty_values):
            alignments.append("right")
        else:
            alignments.append("left")

    return alignments
