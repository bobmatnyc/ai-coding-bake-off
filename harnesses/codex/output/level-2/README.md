# Git Log Analyzer

Level 2 solution for the AI coding bake-off. The project analyzes git history, computes per-author statistics, commit timing patterns, and bus factor, then renders either a terminal summary or JSON.

## Features

- Parses standard `git log --stat` text into typed commit records
- Analyzes real repositories through the `git` CLI
- Computes per-author commits, insertions, deletions, active days, and averages
- Computes time-of-day patterns, weekend activity, weekly and monthly frequency, and longest streaks
- Calculates bus factor from total changed lines
- Supports terminal and JSON output

## Usage

From this directory:

```bash
python3 -m git_analyzer
python3 -m git_analyzer /path/to/repo
python3 -m git_analyzer --format json
python3 -m git_analyzer --since 90
python3 -m git_analyzer --author "Alice"
```

You can also install it locally:

```bash
python3 -m pip install -e .
git-analyzer --format json
```

## Output

Text output includes:

- Repository summary
- Top contributors table
- Bus factor summary
- Commit pattern summary

JSON output contains the same information in structured form for automation.

## Development

Run the local test suite:

```bash
python3 -m pytest tests -v
```

Run the provided benchmark tests from the repository root:

```bash
cd ../../..
python3 -m pytest challenges/level-2-git-analyzer/test_suite -v
```
