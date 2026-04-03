"""Entry point for `python -m git_analyzer`.

Usage:
    python -m git_analyzer [repo] [--format terminal|json] [--since N] [--author NAME]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from git_analyzer.parser import parse_git_log
from git_analyzer.metrics import (
    calculate_author_stats,
    calculate_bus_factor,
    calculate_commit_patterns,
)
from git_analyzer.reporter import format_terminal, format_json


def _build_git_command(
    repo_path: str,
    since_days: int | None,
    author: str | None,
) -> list[str]:
    """Build the git log command arguments.

    Args:
        repo_path: Path to the git repository.
        since_days: If set, limit to commits in the last N days.
        author: If set, filter by author name/email pattern.

    Returns:
        Command list suitable for subprocess.run.
    """
    cmd = [
        "git",
        "-C",
        repo_path,
        "log",
        "--stat",
        "--date=format:%a %b %d %H:%M:%S %Y %z",
    ]

    if since_days is not None:
        since_date = (
            datetime.now(tz=timezone.utc) - timedelta(days=since_days)
        ).strftime("%Y-%m-%d")
        cmd.extend([f"--since={since_date}"])

    if author:
        cmd.extend([f"--author={author}"])

    return cmd


def main() -> None:
    """Main CLI entry point."""
    arg_parser = argparse.ArgumentParser(
        prog="git_analyzer",
        description="Analyze a git repository's commit history and produce insightful metrics.",
    )
    arg_parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    arg_parser.add_argument(
        "--format",
        choices=["terminal", "json"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    arg_parser.add_argument(
        "--since",
        type=int,
        metavar="N",
        help="Limit analysis to the last N days",
    )
    arg_parser.add_argument(
        "--author",
        help="Filter commits by author name or email pattern",
    )

    args = arg_parser.parse_args()

    repo_path = str(Path(args.repo).resolve())

    # Validate the path is a git repository
    check_result = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "--git-dir"],
        capture_output=True,
        text=True,
    )
    if check_result.returncode != 0:
        print(
            f"Error: '{repo_path}' is not a git repository.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Run git log
    cmd = _build_git_command(repo_path, args.since, args.author)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        print("Error: 'git' executable not found. Please install git.", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(f"Error running git log: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    log_text = result.stdout

    # Parse commits
    commits = parse_git_log(log_text)

    if not commits:
        if args.author:
            print(
                f"No commits found for author filter '{args.author}'.",
                file=sys.stderr,
            )
        else:
            print("No commits found in the repository.", file=sys.stderr)
        sys.exit(0)

    # Calculate metrics
    stats = calculate_author_stats(commits)
    bus_factor = calculate_bus_factor(commits)
    patterns = calculate_commit_patterns(commits)

    # Format and output
    if args.format == "json":
        output = format_json(stats, patterns, bus_factor, repo_path)
    else:
        output = format_terminal(stats, patterns, bus_factor, repo_path)

    print(output)


if __name__ == "__main__":
    main()
