"""Git log parsing module.

Parses output from `git log --stat` into structured Commit objects.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Commit:
    """Represents a single git commit with diff statistics."""

    hash: str
    author: str
    email: str
    date: datetime
    message: str
    insertions: int
    deletions: int


# Patterns for parsing git log --stat output
_COMMIT_RE = re.compile(r"^commit ([0-9a-f]{40})$")
_AUTHOR_RE = re.compile(r"^Author:\s+(.+?)\s+<([^>]+)>$")
# Accept both iso format dates and the custom date format
_DATE_RE = re.compile(
    r"^Date:\s+(.+)$"
)
_STAT_SUMMARY_RE = re.compile(
    r"^\s*\d+\s+files?\s+changed"
    r"(?:,\s*(\d+)\s+insertions?\(\+\))?"
    r"(?:,\s*(\d+)\s+deletions?\(-\))?"
)

# Date formats to try when parsing
_DATE_FORMATS = [
    "%a %b %d %H:%M:%S %Y %z",   # git log default: Mon Mar 10 09:15:32 2025 +0000
    "%Y-%m-%d %H:%M:%S %z",       # ISO-ish
    "%Y-%m-%dT%H:%M:%S%z",        # ISO 8601
    "%a %b %d %H:%M:%S %Y",       # Without timezone
]


def _parse_date(date_str: str) -> datetime:
    """Parse a git date string into a datetime object."""
    date_str = date_str.strip()

    for fmt in _DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    # Fallback: try dateutil if available
    try:
        from dateutil import parser as dateutil_parser  # type: ignore[import]
        return dateutil_parser.parse(date_str)
    except (ImportError, ValueError):
        pass

    raise ValueError(f"Unable to parse date: {date_str!r}")


def parse_git_log(log_text: str) -> list[Commit]:
    """Parse git log --stat output into a list of Commit objects.

    Args:
        log_text: Raw output from `git log --stat` command.

    Returns:
        List of Commit objects ordered as they appear in the log.

    Example:
        >>> log = open("sample.txt").read()
        >>> commits = parse_git_log(log)
        >>> len(commits)
        10
    """
    if not log_text or not log_text.strip():
        return []

    commits: list[Commit] = []

    # State for current commit being parsed
    current_hash: str | None = None
    current_author: str | None = None
    current_email: str | None = None
    current_date: datetime | None = None
    current_message_lines: list[str] = []
    current_insertions: int = 0
    current_deletions: int = 0
    in_message: bool = False

    def flush_commit() -> None:
        """Save the currently accumulated commit data."""
        if current_hash is None:
            return
        message = "\n".join(current_message_lines).strip()
        commits.append(
            Commit(
                hash=current_hash,
                author=current_author or "",
                email=current_email or "",
                date=current_date or datetime.now(tz=timezone.utc),
                message=message,
                insertions=current_insertions,
                deletions=current_deletions,
            )
        )

    for line in log_text.splitlines():
        commit_match = _COMMIT_RE.match(line)
        if commit_match:
            # Save the previous commit before starting a new one
            flush_commit()
            current_hash = commit_match.group(1)
            current_author = None
            current_email = None
            current_date = None
            current_message_lines = []
            current_insertions = 0
            current_deletions = 0
            in_message = False
            continue

        if current_hash is None:
            continue

        author_match = _AUTHOR_RE.match(line)
        if author_match:
            current_author = author_match.group(1)
            current_email = author_match.group(2)
            continue

        date_match = _DATE_RE.match(line)
        if date_match:
            try:
                current_date = _parse_date(date_match.group(1))
            except ValueError:
                current_date = datetime.now(tz=timezone.utc)
            in_message = False
            continue

        # After the Date: line, blank line precedes the commit message
        if line.strip() == "" and not in_message and current_date is not None:
            in_message = True
            continue

        stat_match = _STAT_SUMMARY_RE.match(line)
        if stat_match:
            ins = stat_match.group(1)
            dels = stat_match.group(2)
            current_insertions = int(ins) if ins else 0
            current_deletions = int(dels) if dels else 0
            in_message = False
            continue

        # Collect message lines (indented by at least 4 spaces in git log)
        if in_message and (line.startswith("    ") or line == ""):
            current_message_lines.append(line[4:] if line.startswith("    ") else "")

    # Don't forget the last commit
    flush_commit()

    return commits
