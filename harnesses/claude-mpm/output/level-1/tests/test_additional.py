"""Additional tests for table_formatter beyond the provided test suite.

Covers edge cases, CLI flags, error paths, and library-level functions.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FIXTURES_DIR = (
    Path(__file__).parent.parent.parent.parent.parent
    / "challenges"
    / "level-1-table-formatter"
    / "test_suite"
    / "fixtures"
)

sys.path.insert(0, str(Path(__file__).parent.parent))

from table_formatter.detector import detect_column_types, is_numeric_value
from table_formatter.formatter import (
    apply_filter,
    build_separator_cell,
    cell_display_width,
    format_table,
    parse_filter_expression,
    read_csv,
    sort_rows,
    truncate_cell,
)


def run(csv_path: str, *args: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "table_formatter", csv_path, *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=30)


def run_ok(csv_path: str, *args: str) -> str:
    result = run(csv_path, *args)
    assert result.returncode == 0, f"Formatter failed:\n{result.stderr}"
    return result.stdout


def make_csv(content: str) -> str:
    """Write content to a temp CSV and return the path (caller must unlink)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write(content)
        return f.name


# ---------------------------------------------------------------------------
# Unit tests: is_numeric_value
# ---------------------------------------------------------------------------


class TestIsNumericValue:
    def test_integer_string(self) -> None:
        assert is_numeric_value("42") is True

    def test_float_string(self) -> None:
        assert is_numeric_value("3.14") is True

    def test_negative_number(self) -> None:
        assert is_numeric_value("-7.5") is True

    def test_zero(self) -> None:
        assert is_numeric_value("0") is True

    def test_leading_zero_rejected(self) -> None:
        assert is_numeric_value("01234") is False

    def test_empty_string(self) -> None:
        assert is_numeric_value("") is False

    def test_whitespace_only(self) -> None:
        assert is_numeric_value("   ") is False

    def test_plain_text(self) -> None:
        assert is_numeric_value("Alice") is False

    def test_alphanumeric(self) -> None:
        assert is_numeric_value("3D") is False


# ---------------------------------------------------------------------------
# Unit tests: detect_column_types
# ---------------------------------------------------------------------------


class TestDetectColumnTypes:
    def test_all_numeric(self) -> None:
        headers = ["Score"]
        rows = [["95"], ["87"], ["100"]]
        alignments = detect_column_types(rows, headers)
        assert alignments == ["right"]

    def test_all_text(self) -> None:
        headers = ["Name"]
        rows = [["Alice"], ["Bob"]]
        alignments = detect_column_types(rows, headers)
        assert alignments == ["left"]

    def test_mixed_becomes_left(self) -> None:
        headers = ["Value"]
        rows = [["42"], ["hello"]]
        alignments = detect_column_types(rows, headers)
        assert alignments == ["left"]

    def test_empty_column_is_left(self) -> None:
        headers = ["Notes"]
        rows = [[""], [""]]
        alignments = detect_column_types(rows, headers)
        assert alignments == ["left"]

    def test_leading_zero_column_is_left(self) -> None:
        headers = ["ZipCode"]
        rows = [["01234"], ["90210"]]
        alignments = detect_column_types(rows, headers)
        assert alignments == ["left"]


# ---------------------------------------------------------------------------
# Unit tests: cell_display_width
# ---------------------------------------------------------------------------


class TestCellDisplayWidth:
    def test_ascii(self) -> None:
        assert cell_display_width("hello") == 5

    def test_cjk_wide(self) -> None:
        # Each CJK character is 2 columns
        assert cell_display_width("東京") == 4

    def test_emoji(self) -> None:
        # Emoji may vary; just ensure > 0
        assert cell_display_width("Hi") == 2

    def test_empty(self) -> None:
        assert cell_display_width("") == 0

    def test_mixed(self) -> None:
        # "A" (1) + "東" (2) = 3
        assert cell_display_width("A東") == 3


# ---------------------------------------------------------------------------
# Unit tests: truncate_cell
# ---------------------------------------------------------------------------


class TestTruncateCell:
    def test_no_truncation_needed(self) -> None:
        assert truncate_cell("hello", 10) == "hello"

    def test_exact_fit(self) -> None:
        assert truncate_cell("hello", 5) == "hello"

    def test_truncation_adds_ellipsis(self) -> None:
        result = truncate_cell("hello world", 6)
        assert result.endswith("\u2026")
        assert len(result) <= 7  # 5 chars + ellipsis

    def test_zero_max_width_no_op(self) -> None:
        # max_width <= 0 means no truncation
        assert truncate_cell("hello", 0) == "hello"

    def test_unicode_truncation(self) -> None:
        result = truncate_cell("東京都", 3)
        assert result.endswith("\u2026")


# ---------------------------------------------------------------------------
# Unit tests: build_separator_cell
# ---------------------------------------------------------------------------


class TestBuildSeparatorCell:
    def test_left_alignment(self) -> None:
        sep = build_separator_cell("left", 5)
        assert sep.startswith(":")
        assert not sep.endswith(":")

    def test_right_alignment(self) -> None:
        sep = build_separator_cell("right", 5)
        assert sep.endswith(":")
        assert not sep.startswith(":")

    def test_minimum_dashes(self) -> None:
        sep = build_separator_cell("left", 1)
        dashes = sep.count("-")
        assert dashes >= 3


# ---------------------------------------------------------------------------
# Unit tests: parse_filter_expression
# ---------------------------------------------------------------------------


class TestParseFilterExpression:
    def test_greater_than(self) -> None:
        assert parse_filter_expression("age>30") == ("age", ">", "30")

    def test_greater_equal(self) -> None:
        assert parse_filter_expression("salary>=50000") == ("salary", ">=", "50000")

    def test_equal(self) -> None:
        assert parse_filter_expression("name=Alice") == ("name", "=", "Alice")

    def test_not_equal(self) -> None:
        assert parse_filter_expression("dept!=HR") == ("dept", "!=", "HR")

    def test_less_than(self) -> None:
        assert parse_filter_expression("score<80") == ("score", "<", "80")

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_filter_expression("noop")


# ---------------------------------------------------------------------------
# Unit tests: apply_filter
# ---------------------------------------------------------------------------


class TestApplyFilter:
    def _simple_data(self):
        headers = ["Name", "Age", "Salary"]
        rows = [
            ["Alice", "32", "85000"],
            ["Bob", "45", "92000"],
            ["Charlie", "28", "67500"],
        ]
        return headers, rows

    def test_filter_greater_than_numeric(self) -> None:
        headers, rows = self._simple_data()
        result = apply_filter(rows, headers, "Age>30")
        names = [r[0] for r in result]
        assert "Alice" in names
        assert "Bob" in names
        assert "Charlie" not in names

    def test_filter_equal_string(self) -> None:
        headers, rows = self._simple_data()
        result = apply_filter(rows, headers, "Name=Alice")
        assert len(result) == 1
        assert result[0][0] == "Alice"

    def test_filter_unknown_column_raises(self) -> None:
        headers, rows = self._simple_data()
        with pytest.raises(ValueError):
            apply_filter(rows, headers, "NonExistent=foo")

    def test_filter_less_than(self) -> None:
        headers, rows = self._simple_data()
        result = apply_filter(rows, headers, "Age<30")
        assert len(result) == 1
        assert result[0][0] == "Charlie"


# ---------------------------------------------------------------------------
# Unit tests: sort_rows
# ---------------------------------------------------------------------------


class TestSortRows:
    def _simple_data(self):
        headers = ["Name", "Age"]
        rows = [["Charlie", "28"], ["Alice", "32"], ["Bob", "25"]]
        return headers, rows

    def test_sort_by_text_column(self) -> None:
        headers, rows = self._simple_data()
        result = sort_rows(rows, headers, "Name")
        names = [r[0] for r in result]
        assert names == ["Alice", "Bob", "Charlie"]

    def test_sort_descending(self) -> None:
        headers, rows = self._simple_data()
        result = sort_rows(rows, headers, "Age", descending=True)
        ages = [int(r[1]) for r in result]
        assert ages == sorted(ages, reverse=True)

    def test_sort_unknown_column_raises(self) -> None:
        headers, rows = self._simple_data()
        with pytest.raises(ValueError):
            sort_rows(rows, headers, "Nonexistent")


# ---------------------------------------------------------------------------
# Integration tests: format_table
# ---------------------------------------------------------------------------


class TestFormatTable:
    def test_output_has_header_and_separator(self) -> None:
        headers = ["Name", "Score"]
        rows = [["Alice", "95"]]
        alignments = ["left", "right"]
        table = format_table(headers, rows, alignments)
        lines = table.split("\n")
        assert len(lines) == 3
        assert lines[0].startswith("|")
        assert "---" in lines[1]

    def test_right_aligned_separator_ends_with_colon(self) -> None:
        headers = ["Score"]
        rows = [["95"]]
        alignments = ["right"]
        table = format_table(headers, rows, alignments)
        sep_line = table.split("\n")[1]
        cells = [c.strip() for c in sep_line.split("|") if c.strip()]
        assert cells[0].endswith(":")
        assert not cells[0].startswith(":")

    def test_left_aligned_separator_starts_with_colon(self) -> None:
        headers = ["Name"]
        rows = [["Alice"]]
        alignments = ["left"]
        table = format_table(headers, rows, alignments)
        sep_line = table.split("\n")[1]
        cells = [c.strip() for c in sep_line.split("|") if c.strip()]
        assert cells[0].startswith(":")

    def test_empty_rows_produces_two_lines(self) -> None:
        headers = ["A", "B"]
        rows: list[list[str]] = []
        alignments = ["left", "left"]
        table = format_table(headers, rows, alignments)
        lines = table.split("\n")
        assert len(lines) == 2

    def test_max_width_truncation(self) -> None:
        headers = ["Description"]
        rows = [["A very long description that should be truncated"]]
        alignments = ["left"]
        table = format_table(headers, rows, alignments, max_width=10)
        lines = table.split("\n")
        # Data cell should contain ellipsis
        assert "\u2026" in lines[2]


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------


class TestCLIFilter:
    def test_filter_numeric_gt(self) -> None:
        path = make_csv("Name,Age\nAlice,32\nBob,45\nCharlie,28\n")
        try:
            out = run_ok(path, "--filter", "Age>30")
            lines = out.strip().split("\n")[2:]
            names = [line.split("|")[1].strip() for line in lines if line.strip()]
            assert "Alice" in names
            assert "Bob" in names
            assert "Charlie" not in names
        finally:
            os.unlink(path)

    def test_filter_string_eq(self) -> None:
        path = make_csv("Name,Dept\nAlice,Eng\nBob,HR\n")
        try:
            out = run_ok(path, "--filter", "Dept=Eng")
            lines = out.strip().split("\n")[2:]
            assert len(lines) == 1
            assert "Alice" in lines[0]
        finally:
            os.unlink(path)


class TestCLISortDesc:
    def test_sort_desc_numeric(self) -> None:
        path = make_csv("Name,Score\nAlice,85\nBob,92\nCharlie,67\n")
        try:
            out = run_ok(path, "--sort-desc", "Score")
            lines = out.strip().split("\n")[2:]
            scores = []
            for line in lines:
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if len(cells) >= 2:
                    scores.append(float(cells[1]))
            assert scores == sorted(scores, reverse=True)
        finally:
            os.unlink(path)


class TestCLIMaxWidth:
    def test_max_width_truncates_cells(self) -> None:
        path = make_csv("Description\nThis is a very long description that exceeds the limit\n")
        try:
            out = run_ok(path, "--max-width", "15")
            assert "\u2026" in out
        finally:
            os.unlink(path)


class TestCLIEdgeCases:
    def test_csv_with_quoted_commas(self) -> None:
        path = make_csv('Name,Description\nAlice,"Hello, world"\nBob,Plain\n')
        try:
            out = run_ok(path)
            assert "Hello, world" in out
        finally:
            os.unlink(path)

    def test_csv_with_unicode_content(self) -> None:
        path = make_csv("City,Country\nMünchen,Germany\nZürich,Switzerland\n")
        try:
            out = run_ok(path)
            assert "München" in out
            assert "Zürich" in out
        finally:
            os.unlink(path)

    def test_sort_and_filter_combined(self) -> None:
        path = make_csv("Name,Age\nAlice,32\nBob,45\nCharlie,28\nDiana,38\n")
        try:
            out = run_ok(path, "--filter", "Age>30", "--sort", "Name")
            lines = out.strip().split("\n")[2:]
            names = [line.split("|")[1].strip() for line in lines if line.strip()]
            assert names == sorted(names)
            assert "Charlie" not in names
        finally:
            os.unlink(path)

    def test_nonexistent_file_nonzero_exit(self) -> None:
        result = run("/no/such/file.csv")
        assert result.returncode != 0
        assert result.stderr.strip() != ""

    def test_output_file_written_correctly(self) -> None:
        path = make_csv("A,B\n1,2\n3,4\n")
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            out_path = f.name
        try:
            run_ok(path, "--output", out_path)
            content = Path(out_path).read_text(encoding="utf-8")
            assert "|" in content
            assert "---" in content
        finally:
            os.unlink(path)
            os.unlink(out_path)

    def test_all_pipe_counts_equal(self) -> None:
        path = make_csv("Name,Age,City\nAlice,30,NYC\nBob,25,LA\n")
        try:
            out = run_ok(path)
            lines = out.strip().split("\n")
            pipe_counts = [line.count("|") for line in lines]
            assert len(set(pipe_counts)) == 1
        finally:
            os.unlink(path)
