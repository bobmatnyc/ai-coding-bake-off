# Level 2 Challenge: Git Log Analyzer

## Your Task

Read the problem description at `challenges/level-2-git-analyzer/PROBLEM.md` and build a complete solution.

## Workspace Setup

Create your solution in:
```
agents/{your-agent-name}/level-2/
```

For example:
- Claude MPM → `agents/claude-mpm/level-2/`
- Claude Code → `agents/claude-code/level-2/`
- Cursor → `agents/cursor/level-2/`

This should be a properly structured Python project with `pyproject.toml`, `src/` layout, and `tests/`.

## Time Tracking

Record your timing in `agents/{your-agent-name}/level-2/metadata.json`:

```json
{
  "agent": "claude-mpm",
  "level": 2,
  "start_time": "ISO-8601 timestamp when you begin",
  "end_time": "ISO-8601 timestamp when you finish",
  "wall_clock_minutes": null,
  "estimated_tokens": null,
  "notes": ""
}
```

## Delivery Checklist

- [ ] Properly packaged Python project with `pyproject.toml`
- [ ] CLI works: `python -m git_analyzer [path] [--format json] [--since N] [--author NAME]`
- [ ] All provided tests pass: run `pytest challenges/level-2-git-analyzer/test_suite/ -v`
- [ ] Per-author statistics (commits, lines, active days)
- [ ] Commit pattern analysis (time-of-day, weekend, frequency)
- [ ] Bus factor calculation
- [ ] Terminal and JSON output formats
- [ ] Additional tests with good coverage
- [ ] README with installation and usage

## Constraints

- **Do NOT look at other agents' solutions**
- Target Python 3.12+
- The tool must work on real git repositories
- The sample fixture is for testing; real usage should invoke git

## Evaluation Note

Your solution will be evaluated using the rubric at:
`challenges/level-2-git-analyzer/evaluation/rubric.md`

Architecture and packaging are weighted more heavily at this level than Level 1.
