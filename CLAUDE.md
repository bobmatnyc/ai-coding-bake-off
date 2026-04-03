# AI Coding Agent Bake-Off

Benchmark suite testing 9 AI coding agents across 5 Python challenges of increasing complexity. Sequel to ["Orchestration Beats Raw Power"](https://hyperdev.matsuoka.com/p/orchestration-beats-raw-power) (Dec 2025).

## Critical Rules

- `challenges/` is **READ-ONLY** during competition — never modify problem files or test suites
- Each agent's workspace is isolated: `agents/{agent-name}/level-{N}/`
- Solutions must be self-contained Python projects within their workspace directory
- **Do NOT look at other agents' solutions** until cross-review phase
- All solutions target Python 3.12+
- Record timing/token metadata in `metadata.json` per solution

## Project Structure

```
ai-coding-bake-off/
├── challenges/          # Problem definitions + test suites (READ-ONLY)
│   ├── level-1-table-formatter/   # ~30 min, single module
│   ├── level-2-git-analyzer/      # ~1 hr, CLI tool with packaging
│   ├── level-3-weather-alerter/   # ~2 hr, API + DB + Docker
│   ├── level-4-doc-pipeline/      # ~3-4 hr, architecture challenge
│   └── level-5-task-board/        # ~6-8 hr, full-stack app
├── agents/              # Agent workspaces (solutions go here)
│   ├── claude-mpm/      # Claude MPM solutions
│   ├── cursor/          # Cursor solutions
│   ├── claude-code/     # Claude Code solutions
│   ├── codex/           # OpenAI Codex solutions
│   ├── gemini/          # Gemini solutions
│   ├── anti-gravity/    # Anti-Gravity solutions
│   ├── augment/         # Augment Code solutions
│   ├── qwen-aider/      # Qwen 2.5 + Aider solutions
│   └── deepseek-aider/  # DeepSeek + Aider solutions
├── prompts/             # Standardized prompts (one per level)
├── evaluation/          # Scoring framework + cross-review
│   ├── automated/       # Python scripts for metrics
│   ├── cross_review/    # Blind review protocol
│   └── results/         # Collected scores
├── scripts/             # Helpers (setup, metrics, reports)
└── docs/                # Publication materials
```

## Workflows

### Competing (as Claude MPM agent)

1. Read prompt: `prompts/level-{N}-prompt.md`
2. Read problem: `challenges/level-{N}-*/PROBLEM.md`
3. Build solution in: `agents/claude-mpm/level-{N}/`
4. Run provided tests: `pytest challenges/level-{N}-*/test_suite/ -v`
5. Write additional tests in your solution
6. Record metadata in `agents/claude-mpm/level-{N}/metadata.json`

### Evaluating (cross-review mode)

1. Read rubric: `challenges/level-{N}-*/evaluation/rubric.md`
2. Read review protocol: `evaluation/cross_review/review_prompt.md`
3. Evaluate assigned (anonymized) solutions
4. Write reviews to `evaluation/results/`

### Running Automated Evaluation

```bash
python evaluation/automated/run_tests.py        # Test all solutions
python evaluation/automated/code_quality.py      # Ruff + mypy scoring
python evaluation/automated/coverage_check.py    # Coverage analysis
python scripts/collect_metrics.py                # Aggregate all metrics
python scripts/generate_report.py                # Generate comparison report
```

## Code Standards

- Python 3.12+, type hints on all public functions
- pytest for testing, ruff for linting, mypy for type checking
- Docstrings on modules, classes, and public functions
- Every solution includes README.md with setup and usage

## Metadata Format

Every solution includes `metadata.json`:

```json
{
  "agent": "claude-mpm",
  "level": 1,
  "start_time": "2026-04-03T10:00:00Z",
  "end_time": "2026-04-03T10:28:00Z",
  "wall_clock_minutes": 28,
  "estimated_tokens": 15000,
  "model": "claude-opus-4-0520",
  "orchestration_level": "high",
  "notes": "Observations about the process"
}
```

## The 9 Agents

| Agent | Type | Orchestration Level |
|-------|------|-------------------|
| Claude MPM | Multi-agent orchestrated | High |
| Claude Code | CLI agent with tool use | Medium |
| Cursor | IDE-integrated | Low-Medium |
| Codex (OpenAI) | API-based | Low |
| Gemini 2.5 Pro | Long-context single model | Low-Medium |
| Anti-Gravity | Multi-agent framework | High |
| Augment Code | Opus-based code agent | Medium |
| Qwen 2.5 + Aider | Local model + agentic wrapper | Medium |
| DeepSeek + Aider | Local model + agentic wrapper | Medium |

## Publication

Follow-up article to "Orchestration Beats Raw Power". Article outline in `docs/article-outline.md`, methodology in `docs/methodology.md`.
