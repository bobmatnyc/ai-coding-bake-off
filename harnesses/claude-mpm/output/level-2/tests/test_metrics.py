"""Tests for the metrics calculation module."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

import pytest

try:
    from git_analyzer.parser import parse_git_log, Commit
    from git_analyzer.metrics import (
        AuthorStats,
        CommitPatterns,
        calculate_author_stats,
        calculate_bus_factor,
        calculate_commit_patterns,
        calculate_longest_streak,
        _time_of_day,
    )
except ImportError:
    from src.git_analyzer.parser import parse_git_log, Commit  # type: ignore[no-redef]
    from src.git_analyzer.metrics import (  # type: ignore[no-redef]
        AuthorStats,
        CommitPatterns,
        calculate_author_stats,
        calculate_bus_factor,
        calculate_commit_patterns,
        calculate_longest_streak,
        _time_of_day,
    )


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_git_log.txt"


@pytest.fixture
def commits() -> list[Commit]:
    log = FIXTURE_PATH.read_text(encoding="utf-8")
    return parse_git_log(log)


@pytest.fixture
def author_stats(commits: list[Commit]) -> dict[str, AuthorStats]:
    return calculate_author_stats(commits)


# ---------------------------------------------------------------------------
# calculate_author_stats
# ---------------------------------------------------------------------------


def test_author_stats_returns_four_authors(author_stats: dict) -> None:
    assert len(author_stats) == 4


def test_alice_commit_count(author_stats: dict) -> None:
    assert author_stats["Alice Johnson"].commits == 4


def test_bob_commit_count(author_stats: dict) -> None:
    assert author_stats["Bob Smith"].commits == 3


def test_charlie_commit_count(author_stats: dict) -> None:
    assert author_stats["Charlie Brown"].commits == 2


def test_diana_commit_count(author_stats: dict) -> None:
    assert author_stats["Diana Prince"].commits == 1


def test_alice_total_insertions(author_stats: dict) -> None:
    # 247 + 112 + 198 + 18 = 575
    assert author_stats["Alice Johnson"].insertions == 575


def test_alice_total_deletions(author_stats: dict) -> None:
    # 0 + 33 + 0 + 5 = 38
    assert author_stats["Alice Johnson"].deletions == 38


def test_bob_total_insertions(author_stats: dict) -> None:
    # 9 + 52 + 7 = 68
    assert author_stats["Bob Smith"].insertions == 68


def test_bob_total_deletions(author_stats: dict) -> None:
    # 8 + 15 + 5 = 28
    assert author_stats["Bob Smith"].deletions == 28


def test_author_stats_returns_author_stats_instances(author_stats: dict) -> None:
    for v in author_stats.values():
        assert isinstance(v, AuthorStats)


def test_author_active_days_at_least_one(author_stats: dict) -> None:
    for v in author_stats.values():
        assert v.active_days >= 1


def test_first_last_commit_ordering(author_stats: dict) -> None:
    for v in author_stats.values():
        assert v.first_commit <= v.last_commit


def test_alice_first_commit_date(author_stats: dict) -> None:
    alice = author_stats["Alice Johnson"]
    assert alice.first_commit.year == 2025
    assert alice.first_commit.month == 3
    assert alice.first_commit.day == 10


def test_alice_last_commit_date(author_stats: dict) -> None:
    alice = author_stats["Alice Johnson"]
    assert alice.last_commit.day == 17


def test_author_name_in_stats(author_stats: dict) -> None:
    for name, stats in author_stats.items():
        assert stats.author == name


def test_empty_commits_returns_empty_dict() -> None:
    assert calculate_author_stats([]) == {}


# ---------------------------------------------------------------------------
# calculate_bus_factor
# ---------------------------------------------------------------------------


def test_bus_factor_is_integer(commits: list[Commit]) -> None:
    assert isinstance(calculate_bus_factor(commits), int)


def test_bus_factor_between_one_and_four(commits: list[Commit]) -> None:
    bf = calculate_bus_factor(commits)
    assert 1 <= bf <= 4


def test_bus_factor_at_least_one_for_empty() -> None:
    assert calculate_bus_factor([]) == 1


def test_bus_factor_single_author() -> None:
    """One author always gives bus factor of 1."""
    dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
    commits = [
        Commit("a" * 40, "Solo Dev", "solo@ex.com", dt, "init", 100, 0),
        Commit("b" * 40, "Solo Dev", "solo@ex.com", dt, "feat", 50, 10),
    ]
    assert calculate_bus_factor(commits) == 1


def test_bus_factor_evenly_distributed() -> None:
    """When all authors contribute equally, bus factor approaches n/2."""
    dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
    commits = []
    for i, name in enumerate(["A", "B", "C", "D"]):
        commits.append(
            Commit(
                f"{i:040x}",
                name,
                f"{name}@ex.com",
                dt,
                f"commit {i}",
                100,
                0,
            )
        )
    bf = calculate_bus_factor(commits)
    # With 4 equal contributors, need at least 2 to cover 50%
    assert bf >= 2


# ---------------------------------------------------------------------------
# calculate_commit_patterns
# ---------------------------------------------------------------------------


def test_commit_patterns_returns_commit_patterns(commits: list[Commit]) -> None:
    patterns = calculate_commit_patterns(commits)
    assert isinstance(patterns, CommitPatterns)


def test_weekend_commits_equals_one(commits: list[Commit]) -> None:
    """Diana committed on Saturday Mar 15 — that should be the only weekend commit."""
    patterns = calculate_commit_patterns(commits)
    assert patterns.weekend_commits == 1


def test_weekday_commits_equals_nine(commits: list[Commit]) -> None:
    patterns = calculate_commit_patterns(commits)
    assert patterns.weekday_commits == 9


def test_total_commits_equals_ten(commits: list[Commit]) -> None:
    patterns = calculate_commit_patterns(commits)
    total = patterns.weekend_commits + patterns.weekday_commits
    assert total == 10


def test_time_distribution_has_four_keys(commits: list[Commit]) -> None:
    patterns = calculate_commit_patterns(commits)
    assert set(patterns.time_distribution.keys()) == {
        "morning",
        "afternoon",
        "evening",
        "night",
    }


def test_time_distribution_sums_to_ten(commits: list[Commit]) -> None:
    patterns = calculate_commit_patterns(commits)
    assert sum(patterns.time_distribution.values()) == 10


def test_alice_morning_commit() -> None:
    """Alice's 09:15 commit should be classified as morning."""
    dt = datetime(2025, 3, 10, 9, 15, 32, tzinfo=timezone.utc)
    assert _time_of_day(dt) == "morning"


def test_bob_afternoon_commit() -> None:
    """Bob's 14:22 commit should be afternoon."""
    dt = datetime(2025, 3, 10, 14, 22, 10, tzinfo=timezone.utc)
    assert _time_of_day(dt) == "afternoon"


def test_evening_classification() -> None:
    dt = datetime(2025, 1, 1, 18, 30, tzinfo=timezone.utc)
    assert _time_of_day(dt) == "evening"


def test_night_classification_midnight() -> None:
    dt = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert _time_of_day(dt) == "night"


def test_night_classification_before_morning() -> None:
    dt = datetime(2025, 1, 1, 5, 59, tzinfo=timezone.utc)
    assert _time_of_day(dt) == "night"


def test_empty_commits_returns_zero_patterns() -> None:
    patterns = calculate_commit_patterns([])
    assert patterns.weekend_commits == 0
    assert patterns.weekday_commits == 0


# ---------------------------------------------------------------------------
# calculate_longest_streak
# ---------------------------------------------------------------------------


def test_longest_streak_fixture(commits: list[Commit]) -> None:
    """Fixture has commits on Mon/Tue/Wed (Mar 10-12), then Sat (15), then Mon/Tue (17-18)."""
    streak = calculate_longest_streak(commits)
    # Longest consecutive run: Mon 10 → Tue 11 → Wed 12 = 3 days
    assert streak == 3


def test_streak_empty() -> None:
    assert calculate_longest_streak([]) == 0


def test_streak_single_commit() -> None:
    dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
    commits = [Commit("a" * 40, "Dev", "d@e.com", dt, "init", 1, 0)]
    assert calculate_longest_streak(commits) == 1


def test_streak_all_on_same_day() -> None:
    dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
    commits = [
        Commit("a" * 40, "Dev", "d@e.com", dt, "a", 1, 0),
        Commit("b" * 40, "Dev", "d@e.com", dt, "b", 1, 0),
    ]
    assert calculate_longest_streak(commits) == 1


def test_streak_five_consecutive_days() -> None:
    from datetime import timedelta

    base = datetime(2025, 1, 1, tzinfo=timezone.utc)
    commits = [
        Commit(
            f"{i:040x}",
            "Dev",
            "d@e.com",
            base + timedelta(days=i),
            f"commit {i}",
            1,
            0,
        )
        for i in range(5)
    ]
    assert calculate_longest_streak(commits) == 5
