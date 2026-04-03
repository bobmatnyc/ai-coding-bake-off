# Warp: AI Coding Bake-Off

You are **warp**, one of 8 AI coding agents competing in a benchmark. You will solve 5 Python challenges of increasing complexity, then review other agents' solutions.

**IMPORTANT:** Run from the project root (`~/Projects/ai-coding-bake-off/`), NOT from the harness directory. All paths below are relative to the project root.

## Setup

### Prerequisites
- Warp terminal (latest version)
- Warp AI Agent mode enabled
- Python 3.12+

### Configuration
1. Open Warp terminal
2. Navigate to project root: `cd ~/Projects/ai-coding-bake-off`
3. Enter Agent mode (# key or type `/agent`)

## The Bake-Off

### Phase 1: Competition --- Solve All 5 Levels

Work through all 5 challenges in order. Each level is a self-contained Python project.

| Level | Challenge | Time Budget | Complexity |
|-------|-----------|-------------|------------|
| 1 | Markdown Table Formatter | ~30 min | Single module, CLI tool |
| 2 | Git Log Analyzer | ~1 hr | Multi-file package with pyproject.toml |
| 3 | Weather Alerting Service | ~2 hr | REST API + SQLite + Docker |
| 4 | Document Processing Pipeline | ~3-4 hr | Architecture challenge, extensible design |
| 5 | Team Task Board | ~6-8 hr | Full-stack app with auth, WebSocket, CI |

**For each level:**
1. Read the prompt: `prompts/level-{N}-prompt.md`
2. Read the problem: `challenges/level-{N}-*/PROBLEM.md`
3. Read the rubric (know what you're scored on): `challenges/level-{N}-*/evaluation/rubric.md`
4. Build your solution in: `harnesses/warp/output/level-{N}/`
5. Run the provided test suite: `pytest challenges/level-{N}-*/test_suite/ -v`
6. Write additional tests in your solution
7. Record timing in: `harnesses/warp/output/level-{N}/metadata.json`

**Do NOT look at other harnesses' output directories during this phase.**

### Phase 2: Cross-Review --- Evaluate Other Agents

After completing all 5 levels, switch to evaluation mode. You will review other agents' solutions using a blind review protocol.

1. Read the review protocol: `evaluation/cross_review/review_prompt.md`
2. For each level, for each other agent's solution:
   a. Read the rubric: `challenges/level-{N}-*/evaluation/rubric.md`
   b. Read the agent's solution in `harnesses/{other-agent}/output/level-{N}/`
   c. Score against the rubric (1-5 per dimension)
   d. Write your review to `evaluation/results/warp-reviews-{other-agent}-level-{N}.md`
3. Be objective --- score against the rubric, not against your own solution
4. Solutions are evaluated blind where possible

## Paths (all relative to project root)

| What | Path |
|------|------|
| Challenges (READ-ONLY) | `challenges/level-{N}-*/PROBLEM.md` |
| Prompts | `prompts/level-{N}-prompt.md` |
| Rubrics | `challenges/level-{N}-*/evaluation/rubric.md` |
| Your output | `harnesses/warp/output/level-{N}/` |
| Your metadata | `harnesses/warp/output/level-{N}/metadata.json` |
| Review protocol | `evaluation/cross_review/review_prompt.md` |
| Your reviews | `evaluation/results/` |

## Rules

- `challenges/` is READ-ONLY --- never modify problem files or test suites
- All solutions target Python 3.12+ with type hints, tests, docstrings
- Each level solution is a self-contained project in its own directory
- Record timing from first reading the prompt to final commit
- Do NOT look at other harnesses' output during Phase 1

## Metadata Format

Record in `harnesses/warp/output/level-{N}/metadata.json` after each level:

```json
{
  "agent": "warp",
  "level": 1,
  "start_time": "2026-04-03T10:00:00Z",
  "end_time": "2026-04-03T10:28:00Z",
  "wall_clock_minutes": 28,
  "estimated_tokens": 15000,
  "model": "warp-agent",
  "notes": "Observations about the process"
}
```

## Reproducing

1. Clone the repository
2. Install Warp terminal
3. Enter Agent mode and provide the prompt for each level
4. Results appear in `harnesses/warp/output/`
