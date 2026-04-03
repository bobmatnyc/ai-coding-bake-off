"""Metric calculation module for git commit analysis.

Provides functions to calculate per-author statistics, bus factor,
commit patterns (weekend vs weekday, time-of-day distribution), and streaks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from git_analyzer.parser import Commit


@dataclass
class AuthorStats:
    """Statistics for a single author over a range of commits."""

    author: str
    commits: int
    insertions: int
    deletions: int
    active_days: int
    first_commit: datetime
    last_commit: datetime


@dataclass
class CommitPatterns:
    """Distribution patterns for commit timing."""

    weekend_commits: int
    weekday_commits: int
    # Keys: "morning", "afternoon", "evening", "night"
    time_distribution: dict[str, int] = field(default_factory=dict)


def _time_of_day(dt: datetime) -> str:
    """Classify hour of day into a named period.

    Morning:   06:00 – 11:59
    Afternoon: 12:00 – 17:59
    Evening:   18:00 – 20:59
    Night:     21:00 – 05:59
    """
    hour = dt.hour
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 21:
        return "evening"
    else:
        return "night"


def calculate_author_stats(commits: list[Commit]) -> dict[str, AuthorStats]:
    """Calculate per-author commit statistics.

    Args:
        commits: List of parsed Commit objects.

    Returns:
        Dict mapping author name → AuthorStats.

    Example:
        >>> stats = calculate_author_stats(commits)
        >>> stats["Alice Johnson"].commits
        4
    """
    if not commits:
        return {}

    # Accumulate raw data per author
    author_data: dict[str, dict] = {}

    for commit in commits:
        name = commit.author
        if name not in author_data:
            author_data[name] = {
                "commits": 0,
                "insertions": 0,
                "deletions": 0,
                "dates": set(),
                "first_commit": commit.date,
                "last_commit": commit.date,
            }

        data = author_data[name]
        data["commits"] += 1
        data["insertions"] += commit.insertions
        data["deletions"] += commit.deletions
        data["dates"].add(commit.date.date())

        if commit.date < data["first_commit"]:
            data["first_commit"] = commit.date
        if commit.date > data["last_commit"]:
            data["last_commit"] = commit.date

    return {
        name: AuthorStats(
            author=name,
            commits=data["commits"],
            insertions=data["insertions"],
            deletions=data["deletions"],
            active_days=len(data["dates"]),
            first_commit=data["first_commit"],
            last_commit=data["last_commit"],
        )
        for name, data in author_data.items()
    }


def calculate_bus_factor(commits: list[Commit]) -> int:
    """Calculate the bus factor for the repository.

    The bus factor is the minimum number of developers who collectively
    own at least 50% of the total lines changed (insertions + deletions).

    A higher bus factor means the knowledge is spread across more people;
    a bus factor of 1 means one person could cripple the project.

    Args:
        commits: List of parsed Commit objects.

    Returns:
        Integer bus factor (at least 1).

    Example:
        >>> calculate_bus_factor(commits)
        1
    """
    if not commits:
        return 1

    # Count lines changed (insertions + deletions) per author
    author_lines: dict[str, int] = {}
    total_lines = 0

    for commit in commits:
        lines = commit.insertions + commit.deletions
        author_lines[commit.author] = author_lines.get(commit.author, 0) + lines
        total_lines += lines

    if total_lines == 0:
        return max(1, len(set(c.author for c in commits)))

    # Sort authors by contribution (descending)
    sorted_authors = sorted(author_lines.values(), reverse=True)

    # Count how many top contributors own ≥50% of lines
    threshold = total_lines * 0.5
    cumulative = 0
    bus_factor = 0

    for lines in sorted_authors:
        cumulative += lines
        bus_factor += 1
        if cumulative >= threshold:
            break

    return max(1, bus_factor)


def calculate_commit_patterns(commits: list[Commit]) -> CommitPatterns:
    """Analyse commit timing patterns across all commits.

    Args:
        commits: List of parsed Commit objects.

    Returns:
        CommitPatterns with weekend/weekday counts and time distribution.

    Example:
        >>> patterns = calculate_commit_patterns(commits)
        >>> patterns.weekend_commits
        1
    """
    weekend_commits = 0
    weekday_commits = 0
    time_distribution: dict[str, int] = {
        "morning": 0,
        "afternoon": 0,
        "evening": 0,
        "night": 0,
    }

    for commit in commits:
        # weekday() returns 0=Monday … 6=Sunday
        if commit.date.weekday() >= 5:  # Saturday=5, Sunday=6
            weekend_commits += 1
        else:
            weekday_commits += 1

        period = _time_of_day(commit.date)
        time_distribution[period] += 1

    return CommitPatterns(
        weekend_commits=weekend_commits,
        weekday_commits=weekday_commits,
        time_distribution=time_distribution,
    )


def calculate_longest_streak(commits: list[Commit]) -> int:
    """Calculate the longest consecutive-day commit streak.

    Args:
        commits: List of parsed Commit objects.

    Returns:
        Length of the longest streak in calendar days (at least 1 if any commits).

    Example:
        >>> calculate_longest_streak(commits)
        5
    """
    if not commits:
        return 0

    from datetime import timedelta

    commit_dates = sorted({c.date.date() for c in commits})

    if len(commit_dates) == 1:
        return 1

    max_streak = 1
    current_streak = 1

    for i in range(1, len(commit_dates)):
        if commit_dates[i] - commit_dates[i - 1] == timedelta(days=1):
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return max_streak
