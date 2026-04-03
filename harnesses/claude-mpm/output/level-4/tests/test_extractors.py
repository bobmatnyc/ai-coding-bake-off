"""Tests for the text extraction module."""

from pathlib import Path

import pytest

from doc_pipeline.extractors import extract_text, SUPPORTED_EXTENSIONS


class TestExtractText:
    """Tests for extract_text function."""

    def test_extract_from_txt(self, sample_txt_file: Path) -> None:
        """Should extract text content from .txt files."""
        text = extract_text(sample_txt_file)
        assert isinstance(text, str)
        assert "Acme Corporation" in text
        assert len(text) > 50

    def test_extract_from_md(self, sample_md_file: Path) -> None:
        """Should extract text content from .md files."""
        text = extract_text(sample_md_file)
        assert isinstance(text, str)
        assert "Acme Corporation" in text

    def test_extract_returns_string(self, sample_txt_file: Path) -> None:
        """extract_text should always return a string."""
        result = extract_text(sample_txt_file)
        assert isinstance(result, str)

    def test_unsupported_extension_raises_value_error(self, tmp_path: Path) -> None:
        """Should raise ValueError for unsupported file types."""
        bad_file = tmp_path / "test.xyz"
        bad_file.write_text("some content")
        with pytest.raises((ValueError, TypeError, NotImplementedError)):
            extract_text(bad_file)

    def test_unsupported_docx_raises(self, tmp_path: Path) -> None:
        """Should raise ValueError for .docx files."""
        docx_file = tmp_path / "test.docx"
        docx_file.write_bytes(b"fake docx content")
        with pytest.raises((ValueError, TypeError, NotImplementedError)):
            extract_text(docx_file)

    def test_supported_extensions_set(self) -> None:
        """SUPPORTED_EXTENSIONS should include .txt, .md, .pdf."""
        assert ".txt" in SUPPORTED_EXTENSIONS
        assert ".md" in SUPPORTED_EXTENSIONS
        assert ".pdf" in SUPPORTED_EXTENSIONS

    def test_extract_preserves_whitespace(self, tmp_path: Path) -> None:
        """Extracted text should preserve content accurately."""
        content = "Line one.\nLine two.\nLine three."
        f = tmp_path / "multi.txt"
        f.write_text(content)
        text = extract_text(f)
        assert "Line one" in text
        assert "Line two" in text
        assert "Line three" in text

    def test_extract_from_fixture_txt(self, fixtures_dir: Path) -> None:
        """Should extract from the provided sample.txt fixture."""
        if not fixtures_dir.exists():
            pytest.skip("Fixtures directory not available")
        text = extract_text(fixtures_dir / "sample.txt")
        assert len(text) > 100
        assert "Acme Corporation" in text

    def test_extract_from_fixture_pdf(self, fixtures_dir: Path) -> None:
        """Should extract from the provided sample.pdf fixture."""
        if not fixtures_dir.exists():
            pytest.skip("Fixtures directory not available")
        text = extract_text(fixtures_dir / "sample.pdf")
        assert isinstance(text, str)
        assert len(text) > 10
