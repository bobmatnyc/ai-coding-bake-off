# Level 1 Challenge: Markdown Table Formatter

## Your Task

Read the problem description at `challenges/level-1-table-formatter/PROBLEM.md` and build a complete solution.

## Workspace Setup

Create your solution in:
```
agents/{your-agent-name}/level-1/
```

Your solution directory should contain all source code, tests, and documentation.

## Time Tracking

Record your timing in `agents/{your-agent-name}/level-1/metadata.json`:

```json
{
  "agent": "{your-agent-name}",
  "level": 1,
  "start_time": "ISO-8601 timestamp when you begin",
  "end_time": "ISO-8601 timestamp when you finish",
  "wall_clock_minutes": null,
  "estimated_tokens": null,
  "notes": ""
}
```

Update `wall_clock_minutes` and `estimated_tokens` when complete.

## Delivery Checklist

Before declaring this challenge complete, ensure you have:

- [ ] A working `table_formatter` module/package
- [ ] CLI entry point: `python -m table_formatter input.csv` works
- [ ] All provided tests pass: `pytest challenges/level-1-table-formatter/test_suite/ -v`
- [ ] At least 5 additional tests you wrote
- [ ] `--sort`, `--filter`, `--output`, and `--max-width` flags implemented
- [ ] Edge cases handled (unicode, empty files, missing values)
- [ ] A README.md with usage instructions
- [ ] `metadata.json` with timing data

## Constraints

- **Do NOT look at other agents' solutions** in `agents/*/level-1/`
- Use only Python standard library plus any packages you choose to install
- Target Python 3.12+
- Aim for clean, typed, well-tested code

## Evaluation Note

Your solution will be evaluated by other AI agents using the rubric at:
`challenges/level-1-table-formatter/evaluation/rubric.md`

The evaluation covers: Correctness (30%), Code Quality (25%), Testing (20%), Error Handling (15%), Architecture (5%), Documentation (5%).

Focus first on correctness and code quality.
