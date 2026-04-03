"""Core Markdown table formatting logic.

Handles column width calculation (including Unicode wide characters),
cell truncation, alignment, and assembling the final table.
"""

from __future__ import annotations

import csv
import unicodedata


def cell_display_width(text: str) -> int:
    """Compute the display width of a string, accounting for wide Unicode characters.

    CJK and other wide characters occupy 2 columns in a monospace font.
    """
    width = 0
    for char in text:
        eaw = unicodedata.east_asian_width(char)
        if eaw in ("W", "F"):  # Wide or Full-width
            width += 2
        else:
            width += 1
    return width


def truncate_cell(text: str, max_width: int) -> str:
    """Truncate a cell to at most max_width display columns.

    Appends the ellipsis character U+2026 if truncation occurs.
    """
    if max_width <= 0:
        return text
    display = cell_display_width(text)
    if display <= max_width:
        return text

    # Need to truncate; reserve 1 column for the ellipsis
    budget = max_width - 1
    result: list[str] = []
    consumed = 0
    for char in text:
        eaw = unicodedata.east_asian_width(char)
        char_width = 2 if eaw in ("W", "F") else 1
        if consumed + char_width > budget:
            break
        result.append(char)
        consumed += char_width
    return "".join(result) + "\u2026"


def pad_cell(text: str, target_width: int) -> str:
    """Right-pad *text* with spaces so its display width equals *target_width*."""
    current = cell_display_width(text)
    pad = max(0, target_width - current)
    return text + " " * pad


def build_separator_cell(alignment: str, width: int) -> str:
    """Build a separator cell (e.g. `:---`, `---:`) for a given alignment and width.

    *width* is the column content width (not including surrounding spaces).
    Minimum dashes: 3.
    """
    dashes = max(3, width)
    if alignment == "right":
        return "-" * dashes + ":"
    else:
        return ":" + "-" * dashes


def format_table(
    headers: list[str],
    rows: list[list[str]],
    alignments: list[str],
    max_width: int | None = None,
) -> str:
    """Render a Markdown table from headers, data rows, and per-column alignments.

    Parameters
    ----------
    headers:
        Column header strings.
    rows:
        List of data rows; each row is a list of cell strings.
    alignments:
        Per-column alignment: "left" or "right".
    max_width:
        If provided, truncate cell content to this many display columns.

    Returns
    -------
    str
        The formatted Markdown table (no trailing newline).
    """
    num_cols = len(headers)

    # Optionally truncate
    def maybe_truncate(text: str) -> str:
        if max_width is not None:
            return truncate_cell(text, max_width)
        return text

    proc_headers = [maybe_truncate(h) for h in headers]
    proc_rows = [
        [maybe_truncate(row[i] if i < len(row) else "") for i in range(num_cols)]
        for row in rows
    ]

    # Compute per-column display widths
    col_widths: list[int] = []
    for col_idx in range(num_cols):
        w = cell_display_width(proc_headers[col_idx])
        for row in proc_rows:
            w = max(w, cell_display_width(row[col_idx]))
        # Ensure minimum width for separator (3 dashes + alignment char)
        w = max(w, 3)
        col_widths.append(w)

    def render_row(cells: list[str]) -> str:
        parts: list[str] = []
        for col_idx, cell in enumerate(cells):
            padded = pad_cell(cell, col_widths[col_idx])
            parts.append(f" {padded} ")
        return "|" + "|".join(parts) + "|"

    def render_separator() -> str:
        parts: list[str] = []
        for col_idx in range(num_cols):
            sep = build_separator_cell(alignments[col_idx], col_widths[col_idx])
            parts.append(f" {sep} ")
        return "|" + "|".join(parts) + "|"

    output_lines: list[str] = []
    output_lines.append(render_row(proc_headers))
    output_lines.append(render_separator())
    for row in proc_rows:
        output_lines.append(render_row(row))

    return "\n".join(output_lines)


def parse_filter_expression(expr: str) -> tuple[str, str, str]:
    """Parse a filter expression like 'age>30', 'name=Alice', 'salary>=50000'.

    Returns (column, operator, value).
    Raises ValueError if the expression cannot be parsed.
    """
    # Order matters: check two-char operators before one-char
    for op in (">=", "<=", "!=", ">", "<", "="):
        idx = expr.find(op)
        if idx > 0:
            col = expr[:idx].strip()
            val = expr[idx + len(op) :].strip()
            return col, op, val
    raise ValueError(f"Cannot parse filter expression: {expr!r}")


def apply_filter(
    rows: list[list[str]],
    headers: list[str],
    expression: str,
) -> list[list[str]]:
    """Filter rows by an expression.

    Supports: >, <, >=, <=, =, != for both numeric and string comparisons.
    Returns the filtered rows.
    Raises ValueError for invalid expressions or unknown columns.
    """
    col_name, op, value = parse_filter_expression(expression)

    # Find column index (case-insensitive match)
    col_idx: int | None = None
    for i, h in enumerate(headers):
        if h.strip().lower() == col_name.lower():
            col_idx = i
            break
    if col_idx is None:
        raise ValueError(f"Unknown column: {col_name!r}")

    def matches(row: list[str]) -> bool:
        cell = row[col_idx] if col_idx < len(row) else ""  # type: ignore[index]
        # Try numeric comparison first
        try:
            cell_num = float(cell)
            val_num = float(value)
            if op == ">":
                return cell_num > val_num
            elif op == "<":
                return cell_num < val_num
            elif op == ">=":
                return cell_num >= val_num
            elif op == "<=":
                return cell_num <= val_num
            elif op == "=":
                return cell_num == val_num
            elif op == "!=":
                return cell_num != val_num
        except ValueError:
            pass
        # String comparison
        if op == "=":
            return cell == value
        elif op == "!=":
            return cell != value
        elif op == ">":
            return cell > value
        elif op == "<":
            return cell < value
        elif op == ">=":
            return cell >= value
        elif op == "<=":
            return cell <= value
        return False

    return [row for row in rows if matches(row)]


def sort_rows(
    rows: list[list[str]],
    headers: list[str],
    column: str,
    descending: bool = False,
) -> list[list[str]]:
    """Sort rows by the given column name.

    Tries numeric sort first; falls back to string sort.
    Raises ValueError for unknown column names.
    """
    col_idx: int | None = None
    for i, h in enumerate(headers):
        if h.strip().lower() == column.lower():
            col_idx = i
            break
    if col_idx is None:
        raise ValueError(f"Unknown column for sorting: {column!r}")

    def sort_key(row: list[str]) -> tuple:
        cell = row[col_idx] if col_idx < len(row) else ""  # type: ignore[index]
        try:
            return (0, float(cell), "")
        except ValueError:
            return (1, 0.0, cell.lower())

    return sorted(rows, key=sort_key, reverse=descending)


def read_csv(path: str) -> tuple[list[str], list[list[str]]]:
    """Read a CSV file and return (headers, rows).

    Raises FileNotFoundError if the file does not exist.
    Raises ValueError if the file is empty or has no headers.
    """
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        rows_raw = list(reader)

    if not rows_raw:
        raise ValueError(f"CSV file is empty: {path!r}")

    headers = rows_raw[0]
    data_rows = rows_raw[1:]
    return headers, data_rows
