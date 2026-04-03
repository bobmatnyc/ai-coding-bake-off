"""Text extraction module for various file formats."""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def extract_text(path: Path) -> str:
    """Extract text from a file. Supports .txt, .md, .pdf.

    Args:
        path: Path to the file to extract text from.

    Returns:
        Extracted text as a string.

    Raises:
        ValueError: If the file extension is not supported.
        FileNotFoundError: If the file does not exist.
    """
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix!r}. Supported types: {SUPPORTED_EXTENSIONS}")

    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8")

    elif suffix == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            try:
                import pdfplumber  # type: ignore[import]
                with pdfplumber.open(path) as pdf:
                    return "\n".join(p.extract_text() or "" for p in pdf.pages)
            except ImportError:
                raise RuntimeError(
                    "Install pypdf or pdfplumber: pip install pypdf"
                )

    # Should never reach here since we check suffix above
    raise ValueError(f"Unsupported file type: {suffix!r}")
