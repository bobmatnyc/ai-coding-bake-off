# AI Coding Agent Bake-Off: Benchmarking the Future of Software Engineering

> A follow-up to "Orchestration Beats Raw Power" --- measuring how AI coding agents perform across challenges of increasing complexity.

**Author:** Bob Matsuoka, CTO @ Duetto  
**Date:** April 2026  
**Status:** DRAFT

---

## Background: The Original Experiment

In December 2025, we published ["Orchestration Beats Raw Power"](https://hyperdev.matsuoka.com/p/orchestration-beats-raw-power) --- a benchmark of five AI coding systems on three Python tasks. The key finding: **Claude MPM scored 96.2% while Gemini CLI scored 44.3%**, despite near-identical SWE-bench scores. The 52-point performance gap was invisible to industry benchmarks.

But that experiment had limitations:

- **Only 3 tasks** --- too small a sample to be definitive
- **Tasks were small** --- FizzBuzz through async rate limiter (minutes, not hours)
- **No architectural challenges** --- nothing tested system design or multi-file coordination
- **Limited agent roster** --- missing Cursor, local models, and newer tools

This bake-off addresses all of those limitations with 5 challenges spanning 30 minutes to 8 hours, testing everything from basic code generation to full-stack application delivery.

## Overview

This benchmark suite tests AI coding agents across five Python challenges of increasing complexity. Each agent attempts the same problems independently, and then cross-evaluates other agents' solutions. The goal is to produce a rigorous, reproducible comparison of today's leading AI coding tools.

## Thesis

**Orchestrated multi-agent systems outperform single-model approaches, and the advantage grows with problem complexity.**

At Level 1 (a simple formatter), all agents perform similarly. By Level 5 (a full-stack application), the gap between orchestrated and single-model agents becomes a chasm. This benchmark measures exactly where the crossover happens and quantifies the cost-benefit tradeoff.

## The Agents

| Agent | Type | Model(s) | Orchestration |
|-------|------|----------|---------------|
| **Cursor** | IDE-integrated | Claude/GPT-4 | Tab, Composer, multi-file |
| **Claude Code** | CLI agent | Claude Opus/Sonnet | Single agent, tool use |
| **Claude MPM** | Multi-agent | Claude Opus/Sonnet | PM + specialist agents |
| **Codex** | CLI agent | OpenAI Codex | Single agent, sandboxed |
| **Gemini CLI** | CLI agent | Gemini 2.5 Pro | Single agent, tool use |
| **Anti-Gravity** | VS Code extension | Claude/GPT | Agentic IDE extension |
| **Qwen + Aider** | Terminal + editor | Qwen 3 (local) | Aider orchestration |
| **DeepSeek + Aider** | Terminal + editor | DeepSeek V3 (local) | Aider orchestration |
| **Augment Code** | IDE-integrated | Proprietary | Agentic IDE extension |

## The Challenges

| Level | Challenge | Time Budget | Complexity | Key Evaluation Focus |
|-------|-----------|-------------|------------|---------------------|
| 1 | Markdown Table Formatter | ~30 min | Low | Correctness, code quality |
| 2 | Git Log Analyzer | ~1 hr | Low-Medium | Project structure, packaging |
| 3 | Weather Alerting Service | ~2 hr | Medium | API integration, architecture |
| 4 | Document Processing Pipeline | ~3-4 hr | High | Extensibility, design patterns |
| 5 | Team Task Board | ~6-8 hr | Very High | Full-stack, real-time, DevOps |

## Evaluation Framework

Each solution is scored on seven dimensions (1-5 scale):

1. **Correctness** --- Does it work? Does it pass the test suite?
2. **Code Quality** --- Clean code, type hints, linting compliance
3. **Architecture** --- Appropriate patterns, separation of concerns
4. **Testing** --- Agent-written tests, coverage, edge cases
5. **Error Handling** --- Graceful failures, edge case coverage
6. **Documentation** --- README, docstrings, setup instructions
7. **Bonus** --- Level-specific criteria (packaging, Docker, extensibility, real-time)

Weights shift by level: correctness dominates at L1-2, architecture dominates at L4-5.

### Automated Evaluation

```bash
# Run all test suites against all agent solutions
python evaluation/automated/run_tests.py

# Run code quality checks (ruff, mypy)
python evaluation/automated/code_quality.py

# Generate coverage reports
python evaluation/automated/coverage_check.py

# Collect timing and token metrics
python evaluation/automated/metrics.py
```

### Cross-Agent Review

Each agent reviews two other agents' solutions using a standardized prompt and rubric. This produces blind peer-review scores in addition to automated metrics.

## How to Run

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (for Level 3-5)
- Git
- The agent tools you want to benchmark

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/ai-coding-bake-off.git
cd ai-coding-bake-off

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"
```

### Running a Benchmark

```bash
# 1. Set up a harness workspace
./scripts/setup_agent_workspace.sh claude-code

# 2. Give the agent the prompt for a level
#    (Each agent reads from prompts/level-X-prompt.md)

# 3. After all agents complete, run evaluation
python scripts/collect_metrics.py

# 4. Generate comparison report
python scripts/generate_report.py
```

## Results

> Results will be published after all agent runs are complete. Check back for the full analysis.

## Repository Structure

```
ai-coding-bake-off/
├── challenges/          # Problem definitions (read-only for agents)
├── harnesses/           # Each agent's workspace (instructions + output)
├── prompts/             # Standardized prompts per challenge level
├── evaluation/          # Automated scoring and cross-review framework
├── scripts/             # Helper scripts for setup and reporting
└── docs/                # Article materials and methodology
```

## Contributing

This is a benchmark project --- contributions welcome for:

- Additional challenge levels
- New agents to benchmark
- Improved evaluation rubrics
- Better automated scoring
- Statistical analysis tools

Please open an issue before submitting a PR to discuss your proposed contribution.

## License

MIT License. See individual agent solutions for their respective licenses.
