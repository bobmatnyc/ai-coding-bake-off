# git-analyzer

Analyze a git repository's commit history and produce insightful metrics: per-author stats, commit patterns, and bus factor.

## Installation

```bash
pip install -e ".[dev]"
```

Or run directly without installing:

```bash
cd path/to/solution
python3 -m git_analyzer [options]
```

## Usage

```bash
# Analyze current directory
python3 -m git_analyzer

# Analyze a specific repository
python3 -m git_analyzer /path/to/repo

# Output as JSON
python3 -m git_analyzer --format json

# Limit to last 90 days
python3 -m git_analyzer --since 90

# Filter by author
python3 -m git_analyzer --author "Alice"
```

## Sample Output

```
Git Repository Analysis
=======================
Repository: my-project
Period: 2025-03-10 to 2025-03-18 (8 days)
Total Commits: 10
Total Authors: 4

Top Contributors
----------------
  Author                   Commits   Lines(+)   Lines(-)  Active Days
  Alice Johnson                  4        901          0            4
  Charlie Brown                  2        285          6            2
  Bob Smith                      3         49         28            3
  Diana Prince                   1         39          4            1

Bus Factor: 1 (Alice Johnson own 66.9% of changes)

Commit Patterns
---------------
  Most active day:  Monday
  Most active hour: 09:00-10:00
  Weekend commits:  10.0%
  Longest streak:   3 day(s)
```

## Metrics

| Metric | Description |
|:-------|:------------|
| Commits | Total commits per author |
| Lines(+) | Lines inserted |
| Lines(-) | Lines deleted |
| Active Days | Unique days with commits |
| Bus Factor | Fewest authors owning 50%+ of changes |
| Longest Streak | Consecutive days with commits |

## Running Tests

```bash
# Provided test suite
python3 -m pytest ../../../../challenges/level-2-git-analyzer/test_suite/ -v

# Additional tests
python3 -m pytest tests/ -v
```

## Project Structure

```
src/git_analyzer/
├── __init__.py     # Public API
├── __main__.py     # python3 -m entry point
├── cli.py          # Argument parsing
├── parser.py       # git log parsing + subprocess invocation
├── metrics.py      # Metric calculations (author stats, bus factor, patterns)
└── reporter.py     # Terminal and JSON output formatting
```

## Requirements

- Python 3.12+
- git installed and available on PATH
- No third-party runtime dependencies
