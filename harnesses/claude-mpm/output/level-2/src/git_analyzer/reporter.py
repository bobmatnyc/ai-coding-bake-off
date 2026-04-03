"""Output formatting module for git analysis results.

Provides terminal-friendly and JSON output formatters.
"""

from __future__ import annotations

import json
from datetime import datetime, date

from git_analyzer.metrics import AuthorStats, CommitPatterns


def _format_number(n: int) -> str:
    """Format a number with thousand-separators."""
    return f"{n:,}"


def _bar(value: int, max_value: int, width: int = 20) -> str:
    """Return a simple ASCII progress bar."""
    if max_value == 0:
        return " " * width
    filled = round(value / max_value * width)
    return "█" * filled + "░" * (width - filled)


def format_terminal(
    stats: dict[str, AuthorStats],
    patterns: CommitPatterns,
    bus_factor: int,
    repo_path: str,
) -> str:
    """Format analysis results as a human-readable terminal string.

    Args:
        stats: Dict of author name → AuthorStats from calculate_author_stats.
        patterns: CommitPatterns from calculate_commit_patterns.
        bus_factor: Integer bus factor from calculate_bus_factor.
        repo_path: Path to the git repository (for display purposes).

    Returns:
        Formatted multi-line string suitable for terminal output.
    """
    lines: list[str] = []

    lines.append("=" * 60)
    lines.append(f"  Git Repository Analysis: {repo_path}")
    lines.append("=" * 60)

    # Summary counts
    total_commits = sum(a.commits for a in stats.values())
    total_insertions = sum(a.insertions for a in stats.values())
    total_deletions = sum(a.deletions for a in stats.values())
    total_authors = len(stats)

    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total commits   : {_format_number(total_commits)}")
    lines.append(f"  Total authors   : {_format_number(total_authors)}")
    lines.append(f"  Insertions (+)  : {_format_number(total_insertions)}")
    lines.append(f"  Deletions  (-)  : {_format_number(total_deletions)}")
    lines.append(f"  Bus factor      : {bus_factor}")

    # Commit patterns
    lines.append("")
    lines.append("COMMIT PATTERNS")
    lines.append("-" * 40)
    lines.append(f"  Weekday commits : {_format_number(patterns.weekday_commits)}")
    lines.append(f"  Weekend commits : {_format_number(patterns.weekend_commits)}")

    lines.append("")
    lines.append("  Time-of-day distribution:")
    max_td = max(patterns.time_distribution.values(), default=1)
    for period in ("morning", "afternoon", "evening", "night"):
        count = patterns.time_distribution.get(period, 0)
        bar = _bar(count, max_td)
        lines.append(f"    {period:<12} {bar} {count}")

    # Per-author stats
    lines.append("")
    lines.append("AUTHOR STATISTICS")
    lines.append("-" * 40)

    sorted_authors = sorted(stats.values(), key=lambda a: a.commits, reverse=True)
    max_commits = sorted_authors[0].commits if sorted_authors else 1

    for author_stat in sorted_authors:
        bar = _bar(author_stat.commits, max_commits)
        lines.append(f"  {author_stat.author}")
        lines.append(
            f"    Commits     : {_format_number(author_stat.commits)} {bar}"
        )
        lines.append(f"    Insertions  : {_format_number(author_stat.insertions)}")
        lines.append(f"    Deletions   : {_format_number(author_stat.deletions)}")
        lines.append(f"    Active days : {author_stat.active_days}")
        lines.append(
            f"    First commit: {author_stat.first_commit.strftime('%Y-%m-%d')}"
        )
        lines.append(
            f"    Last commit : {author_stat.last_commit.strftime('%Y-%m-%d')}"
        )
        lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)


class _DatetimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime and date objects."""

    def default(self, o: object) -> object:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def format_json(
    stats: dict[str, AuthorStats],
    patterns: CommitPatterns,
    bus_factor: int,
    repo_path: str,
) -> str:
    """Format analysis results as a JSON string.

    Args:
        stats: Dict of author name → AuthorStats from calculate_author_stats.
        patterns: CommitPatterns from calculate_commit_patterns.
        bus_factor: Integer bus factor from calculate_bus_factor.
        repo_path: Path to the git repository (for display purposes).

    Returns:
        JSON-encoded string with full analysis data.
    """
    total_commits = sum(a.commits for a in stats.values())
    total_insertions = sum(a.insertions for a in stats.values())
    total_deletions = sum(a.deletions for a in stats.values())

    authors_data = {
        name: {
            "commits": author_stat.commits,
            "insertions": author_stat.insertions,
            "deletions": author_stat.deletions,
            "active_days": author_stat.active_days,
            "first_commit": author_stat.first_commit,
            "last_commit": author_stat.last_commit,
        }
        for name, author_stat in stats.items()
    }

    payload = {
        "repo_path": repo_path,
        "summary": {
            "total_commits": total_commits,
            "total_authors": len(stats),
            "total_insertions": total_insertions,
            "total_deletions": total_deletions,
            "bus_factor": bus_factor,
        },
        "patterns": {
            "weekend_commits": patterns.weekend_commits,
            "weekday_commits": patterns.weekday_commits,
            "time_distribution": patterns.time_distribution,
        },
        "authors": authors_data,
    }

    return json.dumps(payload, indent=2, cls=_DatetimeEncoder)
