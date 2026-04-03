# git-analyzer

A production-quality Python CLI tool that analyzes a git repository's commit history and produces insightful metrics.

## Features

- Author statistics: commits, insertions, deletions, active days, first/last commit dates
- Bus factor calculation: minimum number of contributors who own 50% of code changes
- Commit patterns: weekday vs. weekend commits, time-of-day distribution
- Longest commit streak across all authors
- Terminal-friendly output with ASCII progress bars
- JSON output for downstream processing

## Installation

```bash
cd output/level-2
pip install -e .
```

Or run directly without installation:

```bash
cd output/level-2
python -m git_analyzer [repo]
```

## Usage

```
usage: git_analyzer [-h] [--format {terminal,json}] [--since N] [--author NAME] [repo]

positional arguments:
  repo                  Path to the git repository (default: current directory)

options:
  -h, --help            show this help message and exit
  --format {terminal,json}
                        Output format (default: terminal)
  --since N             Limit analysis to the last N days
  --author NAME         Filter commits by author name or email pattern
```

## Examples

Analyze the current directory:

```bash
python -m git_analyzer
```

Analyze a specific repository:

```bash
python -m git_analyzer /path/to/repo
```

Analyze commits from the last 30 days:

```bash
python -m git_analyzer /path/to/repo --since 30
```

Filter by author:

```bash
python -m git_analyzer /path/to/repo --author "Alice"
```

Output as JSON:

```bash
python -m git_analyzer /path/to/repo --format json
```

## Sample Terminal Output

```
============================================================
  Git Repository Analysis: /path/to/repo
============================================================

SUMMARY
----------------------------------------
  Total commits   : 10
  Total authors   : 4
  Insertions (+)  : 1,203
  Deletions  (-)  : 72
  Bus factor      : 2

COMMIT PATTERNS
----------------------------------------
  Weekday commits : 9
  Weekend commits : 1

  Time-of-day distribution:
    morning      ████████████████████ 5
    afternoon    ████████████░░░░░░░░ 3
    evening      ████░░░░░░░░░░░░░░░░ 1
    night        ████░░░░░░░░░░░░░░░░ 1

AUTHOR STATISTICS
----------------------------------------
  Alice Johnson
    Commits     : 4 ████████████████████
    Insertions  : 575
    Deletions   : 38
    Active days : 3
    First commit: 2025-03-10
    Last commit : 2025-03-17

  ...
============================================================
```

## Running Tests

```bash
cd output/level-2
python -m pytest tests/ -v
```

## Project Structure

```
output/level-2/
├── pyproject.toml
├── README.md
├── src/
│   └── git_analyzer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── parser.py
│       ├── metrics.py
│       └── reporter.py
└── tests/
    ├── __init__.py
    ├── fixtures/
    │   └── sample_git_log.txt
    ├── test_parser.py
    └── test_metrics.py
```
