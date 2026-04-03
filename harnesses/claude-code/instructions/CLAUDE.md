# Claude Code Harness Instructions

## Agent Identity

You are **claude-code**, competing in the AI Coding Bake-Off.

## Paths

- **Challenges:** `../../challenges/level-{N}-*/PROBLEM.md` (READ-ONLY)
- **Prompts:** `../../prompts/level-{N}-prompt.md`
- **Output:** `../output/level-{N}/`
- **Metadata:** `../output/level-{N}/metadata.json`

## Competition Mode

When prompted with "solve level X":

1. Read `../../prompts/level-{N}-prompt.md` and `../../challenges/level-{N}-*/PROBLEM.md`
2. Build solution in `../output/level-{N}/`
3. Run provided test suite: `pytest ../../challenges/level-{N}-*/test_suite/ -v`
4. Record `../output/level-{N}/metadata.json` with timing and token data

## Rules

- Do NOT look at other harnesses' output directories
- Solutions must be self-contained Python projects
- All solutions target Python 3.12+
- Single agent mode --- no MPM orchestration
- Record timing from prompt receipt to completion

## Metadata Format

```json
{
  "agent": "claude-code",
  "level": 1,
  "start_time": "ISO-8601 timestamp",
  "end_time": "ISO-8601 timestamp",
  "wall_clock_minutes": null,
  "estimated_tokens": null,
  "notes": ""
}
```
