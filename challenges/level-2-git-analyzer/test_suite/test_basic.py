"""Provided test suite for Level 2: Git Log Analyzer.

Tests use a sample git log fixture rather than requiring a real repository.
Agents must pass these tests and should write additional ones.
"""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_LOG = FIXTURES_DIR / "sample_git_log.txt"


def _load_sample_log() -> str:
    """Load the sample git log fixture."""
    return SAMPLE_LOG.read_text()


class TestLogParsing:
    """Test git log parsing functionality."""

    def test_parse_commits_count(self) -> None:
        """Should parse the correct number of commits."""
        # Import the parser - agents decide the module structure
        # We try common import paths
        try:
            from git_analyzer.parser import parse_git_log
        except ImportError:
            from src.git_analyzer.parser import parse_git_log

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)

        assert len(commits) == 10, f"Expected 10 commits, got {len(commits)}"

    def test_parse_author_names(self) -> None:
        """Should correctly extract author names."""
        try:
            from git_analyzer.parser import parse_git_log
        except ImportError:
            from src.git_analyzer.parser import parse_git_log

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)

        authors = {c.author for c in commits} if hasattr(commits[0], 'author') else {c['author'] for c in commits}
        expected_authors = {"Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince"}

        assert authors == expected_authors, f"Expected {expected_authors}, got {authors}"

    def test_parse_commit_dates(self) -> None:
        """Should parse commit dates correctly."""
        try:
            from git_analyzer.parser import parse_git_log
        except ImportError:
            from src.git_analyzer.parser import parse_git_log

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)

        first = commits[0]
        # Support both object and dict access
        if hasattr(first, 'date'):
            assert first.date is not None, "Commit date should not be None"
        else:
            assert first['date'] is not None, "Commit date should not be None"

    def test_parse_insertions_deletions(self) -> None:
        """Should extract insertion and deletion counts."""
        try:
            from git_analyzer.parser import parse_git_log
        except ImportError:
            from src.git_analyzer.parser import parse_git_log

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)

        # First commit: 247 insertions, 0 deletions
        first = commits[0]
        if hasattr(first, 'insertions'):
            assert first.insertions == 247, f"Expected 247 insertions, got {first.insertions}"
            assert first.deletions == 0, f"Expected 0 deletions, got {first.deletions}"
        else:
            assert first['insertions'] == 247
            assert first['deletions'] == 0


class TestMetrics:
    """Test metric calculations."""

    def test_author_commit_counts(self) -> None:
        """Should correctly count commits per author."""
        try:
            from git_analyzer.parser import parse_git_log
            from git_analyzer.metrics import calculate_author_stats
        except ImportError:
            from src.git_analyzer.parser import parse_git_log
            from src.git_analyzer.metrics import calculate_author_stats

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)
        stats = calculate_author_stats(commits)

        # Alice has 4 commits in the sample
        alice_stats = None
        if isinstance(stats, dict):
            alice_stats = stats.get("Alice Johnson")
        else:
            alice_stats = next((s for s in stats if getattr(s, 'author', None) == "Alice Johnson" or s.get('author') == "Alice Johnson"), None)

        assert alice_stats is not None, "Alice Johnson should be in stats"

        commit_count = alice_stats.commits if hasattr(alice_stats, 'commits') else alice_stats.get('commits', alice_stats.get('commit_count'))
        assert commit_count == 4, f"Alice should have 4 commits, got {commit_count}"

    def test_bus_factor_calculation(self) -> None:
        """Bus factor should be calculated correctly."""
        try:
            from git_analyzer.parser import parse_git_log
            from git_analyzer.metrics import calculate_bus_factor
        except ImportError:
            from src.git_analyzer.parser import parse_git_log
            from src.git_analyzer.metrics import calculate_bus_factor

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)
        bus_factor = calculate_bus_factor(commits)

        # bus_factor should be an integer >= 1
        if isinstance(bus_factor, dict):
            bf_value = bus_factor.get('bus_factor', bus_factor.get('value'))
        elif isinstance(bus_factor, tuple):
            bf_value = bus_factor[0]
        else:
            bf_value = bus_factor

        assert isinstance(bf_value, int), f"Bus factor should be an integer, got {type(bf_value)}"
        assert bf_value >= 1, f"Bus factor should be >= 1, got {bf_value}"
        assert bf_value <= 4, f"Bus factor should be <= total authors (4), got {bf_value}"

    def test_weekend_detection(self) -> None:
        """Should correctly identify weekend commits."""
        try:
            from git_analyzer.parser import parse_git_log
            from git_analyzer.metrics import calculate_commit_patterns
        except ImportError:
            from src.git_analyzer.parser import parse_git_log
            from src.git_analyzer.metrics import calculate_commit_patterns

        log_text = _load_sample_log()
        commits = parse_git_log(log_text)
        patterns = calculate_commit_patterns(commits)

        # Diana's commit on Sat Mar 15 is the only weekend commit
        if isinstance(patterns, dict):
            weekend_count = patterns.get('weekend_commits', patterns.get('weekend', 0))
        else:
            weekend_count = patterns.weekend_commits if hasattr(patterns, 'weekend_commits') else 0

        assert weekend_count == 1, f"Expected 1 weekend commit, got {weekend_count}"
