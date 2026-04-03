# Gemini CLI: AI Coding Bake-Off

## Agent Identity

You are **gemini**, competing in the AI Coding Bake-Off.

## Paths

- Challenges: `../../challenges/level-{N}-*/PROBLEM.md` (READ-ONLY)
- Prompts: `../../prompts/level-{N}-prompt.md`
- Output: `../output/level-{N}/`
- Metadata: `../output/level-{N}/metadata.json`

## Rules

- Read the challenge from the paths above
- Write ALL solution files to `../output/level-{N}/`
- Do NOT look at other harnesses' output directories
- All solutions target Python 3.12+
- Include type hints, docstrings, and tests
- Run provided test suite: `pytest ../../challenges/level-{N}-*/test_suite/ -v`
- Record timing in `../output/level-{N}/metadata.json`

## Metadata Format

```json
{
  "agent": "gemini",
  "level": 1,
  "start_time": "ISO-8601 timestamp",
  "end_time": "ISO-8601 timestamp",
  "wall_clock_minutes": null,
  "estimated_tokens": null,
  "notes": ""
}
```
