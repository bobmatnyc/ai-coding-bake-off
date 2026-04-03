# AI Coding Agent Bake-Off --- Claude Code / MPM Instructions

## Project Purpose

This is a benchmark suite for evaluating AI coding agents. Multiple agents solve the same five Python challenges, and their solutions are cross-evaluated.

## Project Structure

```
ai-coding-bake-off/
├── challenges/          # READ-ONLY problem definitions and test suites
├── agents/              # Agent workspaces --- solutions go here
├── prompts/             # Standardized prompts (one per level)
├── evaluation/          # Scoring framework and cross-review tools
├── scripts/             # Helper scripts
└── docs/                # Publication materials
```

## How to Work on Challenges

### As a Competing Agent

1. Read the prompt at `prompts/level-X-prompt.md`
2. Read the problem at `challenges/level-X-*/PROBLEM.md`
3. Create your solution in `agents/claude-code/level-X/` (or `agents/claude-mpm/level-X/`)
4. Run the provided test suite: `pytest challenges/level-X-*/test_suite/`
5. Write your own additional tests
6. Do NOT look at other agents' solutions

### As an Evaluator (Cross-Review)

1. Read the evaluation rubric at `challenges/level-X-*/evaluation/rubric.md`
2. Read the cross-review prompt at `evaluation/cross_review/review_prompt.md`
3. Evaluate the assigned agent's solution
4. Write your review to `evaluation/results/`

## Running Tests

```bash
# Run test suite for a specific level
pytest challenges/level-1-table-formatter/test_suite/ -v

# Run an agent's own tests
pytest agents/claude-code/level-1/tests/ -v

# Run all evaluation scripts
python evaluation/automated/run_tests.py
python evaluation/automated/code_quality.py
python evaluation/automated/coverage_check.py
```

## Important Rules

- **challenges/** is READ-ONLY during competition. Do not modify problem files or test suites.
- **agents/{your-agent}/** is your workspace. All solution code goes here.
- Each level solution should be a self-contained project within `agents/{agent}/level-X/`.
- Record timing metadata in `agents/{agent}/level-X/metadata.json`.
- Do not look at other agents' directories until cross-review phase.

## Metadata Format

Each solution should include `metadata.json`:

```json
{
  "agent": "claude-code",
  "level": 1,
  "start_time": "2026-04-03T10:00:00Z",
  "end_time": "2026-04-03T10:28:00Z",
  "wall_clock_minutes": 28,
  "estimated_tokens": 15000,
  "notes": "Any observations about the process"
}
```

## Code Quality Standards

Solutions should aim for:
- Python 3.12+ compatibility
- Type hints on all public functions
- Passing ruff and mypy checks
- pytest for testing
- Docstrings on modules, classes, and public functions
