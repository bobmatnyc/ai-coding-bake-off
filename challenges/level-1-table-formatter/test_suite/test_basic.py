"""Provided test suite for Level 1: Markdown Table Formatter.

Agents must pass these tests. Agents should also write additional tests.
"""

import csv
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _run_formatter(csv_path: str, *extra_args: str) -> str:
    """Run the table_formatter module and capture stdout."""
    cmd = [sys.executable, "-m", "table_formatter", csv_path, *extra_args]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f"Formatter failed: {result.stderr}"
    return result.stdout


class TestBasicFormatting:
    """Test core table formatting functionality."""

    def test_simple_csv_produces_valid_markdown(self) -> None:
        """Simple CSV should produce a valid Markdown table."""
        output = _run_formatter(str(FIXTURES_DIR / "simple.csv"))
        lines = output.strip().split("\n")

        # Must have at least 3 lines: header, separator, one data row
        assert len(lines) >= 3, f"Expected at least 3 lines, got {len(lines)}"

        # Header row starts and ends with pipe
        assert lines[0].startswith("|"), "Header row must start with |"
        assert lines[0].rstrip().endswith("|"), "Header row must end with |"

        # Separator row contains dashes
        assert "---" in lines[1], "Second line must be a separator row"

        # All lines have same number of pipes
        pipe_counts = [line.count("|") for line in lines]
        assert len(set(pipe_counts)) == 1, (
            f"All rows must have same number of columns. Pipe counts: {pipe_counts}"
        )

    def test_column_count_matches_csv(self) -> None:
        """Output should have the same number of columns as the input CSV."""
        csv_path = FIXTURES_DIR / "simple.csv"
        with open(csv_path) as f:
            reader = csv.reader(f)
            headers = next(reader)
            expected_cols = len(headers)

        output = _run_formatter(str(csv_path))
        first_line = output.strip().split("\n")[0]
        # Count columns by splitting on | and removing empty first/last
        actual_cols = len([c for c in first_line.split("|") if c.strip()])

        assert actual_cols == expected_cols, (
            f"Expected {expected_cols} columns, got {actual_cols}"
        )

    def test_all_data_rows_present(self) -> None:
        """Every data row from the CSV should appear in the output."""
        csv_path = FIXTURES_DIR / "simple.csv"
        with open(csv_path) as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            data_rows = list(reader)

        output = _run_formatter(str(csv_path))
        lines = output.strip().split("\n")
        # Subtract header and separator
        output_data_lines = lines[2:]

        assert len(output_data_lines) == len(data_rows), (
            f"Expected {len(data_rows)} data rows, got {len(output_data_lines)}"
        )

    def test_numeric_columns_right_aligned(self) -> None:
        """Numeric columns should use right-alignment in the separator."""
        output = _run_formatter(str(FIXTURES_DIR / "simple.csv"))
        separator = output.strip().split("\n")[1]
        cells = [c.strip() for c in separator.split("|") if c.strip()]

        # At least one cell should have right-alignment (ending with :)
        # simple.csv has numeric columns
        right_aligned = [c for c in cells if c.endswith(":") and not c.startswith(":")]
        assert len(right_aligned) > 0, (
            "Expected at least one right-aligned (numeric) column"
        )


class TestEdgeCases:
    """Test edge case handling."""

    def test_unicode_csv(self) -> None:
        """Unicode characters should be handled correctly."""
        output = _run_formatter(str(FIXTURES_DIR / "unicode.csv"))
        lines = output.strip().split("\n")

        assert len(lines) >= 3, "Unicode CSV should produce valid output"
        # Check that unicode content is present
        full_output = output.lower()
        assert "tokyo" in full_output or "東京" in output, (
            "Unicode content should be preserved"
        )

    def test_edge_cases_csv(self) -> None:
        """Edge cases (empty cells, long content) should not crash."""
        output = _run_formatter(str(FIXTURES_DIR / "edge_cases.csv"))
        lines = output.strip().split("\n")

        assert len(lines) >= 3, "Edge cases CSV should produce valid output"

    def test_empty_csv_produces_header_only(self) -> None:
        """A CSV with headers but no data should still produce a valid table."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            f.write("Name,Age,City\n")
            temp_path = f.name

        try:
            output = _run_formatter(temp_path)
            lines = output.strip().split("\n")
            # Should have header and separator at minimum
            assert len(lines) >= 2, "Empty CSV should produce header + separator"
        finally:
            os.unlink(temp_path)

    def test_nonexistent_file_returns_error(self) -> None:
        """Attempting to format a nonexistent file should fail gracefully."""
        result = subprocess.run(
            [sys.executable, "-m", "table_formatter", "/tmp/nonexistent_file.csv"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode != 0, "Should return non-zero exit code for missing file"


class TestCLIOptions:
    """Test CLI flags."""

    def test_output_to_file(self) -> None:
        """--output flag should write to a file."""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            _run_formatter(
                str(FIXTURES_DIR / "simple.csv"), "--output", output_path
            )
            assert os.path.exists(output_path), "Output file should be created"
            with open(output_path) as f:
                content = f.read()
            assert "|" in content, "Output file should contain a Markdown table"
        finally:
            os.unlink(output_path)

    def test_sort_flag(self) -> None:
        """--sort flag should sort the output rows."""
        output = _run_formatter(str(FIXTURES_DIR / "simple.csv"), "--sort", "Name")
        lines = output.strip().split("\n")[2:]  # skip header + separator

        # Extract first column values
        names = []
        for line in lines:
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if cells:
                names.append(cells[0])

        assert names == sorted(names), f"Rows should be sorted by Name: {names}"
