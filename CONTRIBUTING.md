# Contributing to AI Coding Bake-Off

## For AI Agents (Competition)

1. Read your prompt at `prompts/level-{N}-prompt.md`
2. Build your solution in `agents/{your-name}/level-{N}/`
3. Run provided tests and write your own
4. Fill in `metadata.json` with timing data
5. Do NOT look at other agents' work

## For Humans

- Problem definitions in `challenges/` — suggest improvements via PR
- Evaluation scripts in `evaluation/automated/` — bug fixes welcome
- Article drafts in `docs/` — feedback welcome

## Running the Full Benchmark

```bash
make setup-venv              # One-time setup
source .venv/bin/activate
make test-level LEVEL=1      # Test a specific level
make eval-all                # Run all evaluations
make report                  # Generate comparison report
```
