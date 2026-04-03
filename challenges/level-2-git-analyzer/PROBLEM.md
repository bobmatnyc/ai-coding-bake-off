# Level 2: Git Log Analyzer

**Time Budget:** ~1 hour  
**Difficulty:** Low-Medium  
**Focus:** Parsing, project structure, packaging, data aggregation

## Problem Statement

Create a CLI tool that analyzes a git repository's commit history and produces insightful metrics. The tool should parse git log output, compute per-author statistics, detect commit patterns, and calculate the project's bus factor.

## Requirements

### Core Metrics

1. **Per-Author Statistics**:
   - Total commits
   - Lines added / removed
   - Active days (unique days with commits)
   - First and last commit dates
   - Average commits per active day

2. **Commit Patterns**:
   - Time-of-day distribution (morning/afternoon/evening/night)
   - Weekend vs. weekday commits
   - Commit frequency over time (weekly/monthly)
   - Longest streak of consecutive days with commits

3. **Bus Factor**:
   - Calculate the minimum number of developers who own 50% of the codebase (by lines changed)
   - Identify the top contributors by percentage of total changes

4. **Summary Statistics**:
   - Total commits, authors, active period
   - Average commit size (lines changed)
   - Most active day of week
   - Most active hour of day

### CLI Interface

```bash
# Analyze current directory
python -m git_analyzer

# Analyze specific repo
python -m git_analyzer /path/to/repo

# Output as JSON
python -m git_analyzer --format json

# Limit analysis to last N days
python -m git_analyzer --since 90

# Filter by author
python -m git_analyzer --author "Alice"
```

### Output Format

**Terminal output** should be a well-formatted summary with sections and aligned columns. Example:

```
Git Repository Analysis
=======================
Repository: my-project
Period: 2024-01-15 to 2026-03-28 (803 days)
Total Commits: 1,247
Total Authors: 8

Top Contributors
----------------
  Author              Commits   Lines(+)   Lines(-)   Active Days
  Alice Johnson           423     45,210     12,340          189
  Bob Smith               312     28,100      9,870          156
  ...

Bus Factor: 2 (Alice Johnson, Bob Smith own 58.9% of changes)

Commit Patterns
---------------
  Most active day:  Wednesday
  Most active hour: 14:00-15:00
  Weekend commits:  4.2%
```

**JSON output** should be a structured object with all metrics.

### Project Structure

The solution must be a properly structured Python project:

```
git_analyzer/
├── pyproject.toml          # Project metadata, dependencies, entry points
├── README.md               # Usage, installation, examples
├── src/
│   └── git_analyzer/
│       ├── __init__.py
│       ├── __main__.py     # CLI entry point
│       ├── parser.py       # Git log parsing
│       ├── metrics.py      # Metric calculations
│       └── reporter.py     # Output formatting
└── tests/
    ├── test_parser.py
    ├── test_metrics.py
    └── fixtures/
        └── sample_git_log.txt
```

## Deliverables

1. A properly packaged Python project with `pyproject.toml`
2. CLI tool runnable via `python -m git_analyzer`
3. Terminal and JSON output formats
4. Tests with good coverage
5. README with installation and usage instructions

## Open Decisions (Agent's Choice)

- How to invoke git (subprocess, gitpython, dulwich, etc.)
- Whether to parse `git log` text output or use a library
- Report formatting and layout
- Whether to add visualization (matplotlib charts, sparklines)
- Caching strategy for repeated analysis
- How to handle merge commits

## Evaluation Criteria

See `evaluation/rubric.md` for the full scoring rubric. Key weights for this level:

- **Correctness**: 25%
- **Code Quality**: 20%
- **Architecture**: 15%
- **Testing**: 15%
- **Error Handling**: 10%
- **Documentation**: 10%
- **Bonus (Packaging)**: 5%
