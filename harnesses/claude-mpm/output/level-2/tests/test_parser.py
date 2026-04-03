"""Tests for the git log parser module."""

from __future__ import annotations

from pathlib import Path

import pytest

try:
    from git_analyzer.parser import parse_git_log, Commit
except ImportError:
    from src.git_analyzer.parser import parse_git_log, Commit  # type: ignore[no-redef]


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_git_log.txt"


@pytest.fixture
def sample_log() -> str:
    return FIXTURE_PATH.read_text(encoding="utf-8")


@pytest.fixture
def commits(sample_log: str) -> list[Commit]:
    return parse_git_log(sample_log)


# ---------------------------------------------------------------------------
# Basic parsing
# ---------------------------------------------------------------------------


def test_parses_exactly_ten_commits(commits: list[Commit]) -> None:
    assert len(commits) == 10


def test_all_commits_are_commit_instances(commits: list[Commit]) -> None:
    for c in commits:
        assert isinstance(c, Commit)


def test_first_commit_hash(commits: list[Commit]) -> None:
    assert commits[0].hash == "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"


def test_last_commit_hash(commits: list[Commit]) -> None:
    assert commits[-1].hash == "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e6"


def test_all_hashes_are_forty_chars(commits: list[Commit]) -> None:
    for c in commits:
        assert len(c.hash) == 40, f"Hash {c.hash!r} is not 40 chars"


def test_unique_hashes(commits: list[Commit]) -> None:
    hashes = [c.hash for c in commits]
    assert len(hashes) == len(set(hashes))


# ---------------------------------------------------------------------------
# Author / email extraction
# ---------------------------------------------------------------------------


def test_author_names_extracted(commits: list[Commit]) -> None:
    names = {c.author for c in commits}
    assert names == {"Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince"}


def test_author_emails_extracted(commits: list[Commit]) -> None:
    emails = {c.email for c in commits}
    assert emails == {
        "alice@example.com",
        "bob@example.com",
        "charlie@example.com",
        "diana@example.com",
    }


def test_first_commit_author(commits: list[Commit]) -> None:
    assert commits[0].author == "Alice Johnson"
    assert commits[0].email == "alice@example.com"


def test_diana_commit_author(commits: list[Commit]) -> None:
    diana_commits = [c for c in commits if c.author == "Diana Prince"]
    assert len(diana_commits) == 1
    assert diana_commits[0].email == "diana@example.com"


# ---------------------------------------------------------------------------
# Diff statistics
# ---------------------------------------------------------------------------


def test_first_commit_insertions(commits: list[Commit]) -> None:
    """First commit: 247 insertions, 0 deletions."""
    assert commits[0].insertions == 247


def test_first_commit_deletions(commits: list[Commit]) -> None:
    assert commits[0].deletions == 0


def test_second_commit_stats(commits: list[Commit]) -> None:
    """fix: resolve login redirect loop — 9 ins / 8 del."""
    assert commits[1].insertions == 9
    assert commits[1].deletions == 8


def test_diana_commit_insertions(commits: list[Commit]) -> None:
    diana = next(c for c in commits if c.author == "Diana Prince")
    assert diana.insertions == 243
    assert diana.deletions == 0


def test_total_insertions(commits: list[Commit]) -> None:
    total = sum(c.insertions for c in commits)
    # Sum from fixture: 247+9+112+95+198+52+243+222+18+7 = 1203
    assert total == 1203


def test_total_deletions(commits: list[Commit]) -> None:
    total = sum(c.deletions for c in commits)
    # Sum from fixture: 0+8+33+6+0+15+0+0+5+5 = 72
    assert total == 72


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------


def test_dates_are_datetime_objects(commits: list[Commit]) -> None:
    from datetime import datetime

    for c in commits:
        assert isinstance(c.date, datetime), f"Expected datetime, got {type(c.date)}"


def test_first_commit_date(commits: list[Commit]) -> None:
    dt = commits[0].date
    assert dt.year == 2025
    assert dt.month == 3
    assert dt.day == 10
    assert dt.hour == 9
    assert dt.minute == 15


def test_diana_commit_is_saturday(commits: list[Commit]) -> None:
    diana = next(c for c in commits if c.author == "Diana Prince")
    # Saturday = weekday() == 5
    assert diana.date.weekday() == 5


def test_dates_are_timezone_aware(commits: list[Commit]) -> None:
    for c in commits:
        assert c.date.tzinfo is not None, f"Commit {c.hash} has no tzinfo"


# ---------------------------------------------------------------------------
# Message extraction
# ---------------------------------------------------------------------------


def test_first_commit_message(commits: list[Commit]) -> None:
    assert commits[0].message == "feat: add user authentication module"


def test_messages_are_non_empty(commits: list[Commit]) -> None:
    for c in commits:
        assert c.message, f"Commit {c.hash} has empty message"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_empty_log_returns_empty_list() -> None:
    assert parse_git_log("") == []


def test_whitespace_only_log_returns_empty_list() -> None:
    assert parse_git_log("   \n  \n  ") == []


def test_single_commit_no_stats() -> None:
    log = (
        "commit aabbccddeeff0011223344556677889900aabbcc\n"
        "Author: Test User <test@example.com>\n"
        "Date:   Mon Mar 10 09:00:00 2025 +0000\n"
        "\n"
        "    Initial commit\n"
    )
    result = parse_git_log(log)
    assert len(result) == 1
    assert result[0].author == "Test User"
    assert result[0].insertions == 0
    assert result[0].deletions == 0


def test_commit_with_only_insertions() -> None:
    log = (
        "commit aabbccddeeff0011223344556677889900aabbcc\n"
        "Author: Dev <dev@example.com>\n"
        "Date:   Mon Mar 10 09:00:00 2025 +0000\n"
        "\n"
        "    add new file\n"
        "\n"
        " newfile.py | 50 ++++++++++++++++++++\n"
        " 1 file changed, 50 insertions(+)\n"
    )
    result = parse_git_log(log)
    assert result[0].insertions == 50
    assert result[0].deletions == 0
