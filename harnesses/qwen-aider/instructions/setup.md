# Qwen + Aider Harness Setup

## Prerequisites

- aider-chat installed (`pipx install aider-chat`)
- OPENROUTER_API_KEY in project root .env file
- Python 3.12+

## Running a Single Level

```bash
cd harnesses/qwen-aider
./run-level.sh 1    # Solve level 1
```

## Running the Full Bake-Off

```bash
cd harnesses/qwen-aider
./run-bakeoff.sh    # All 5 levels sequentially
```

## How It Works

The launch scripts:
1. Load the API key from ../../.env
2. Pre-load all challenge files into aider's context (PROBLEM.md, rubric, tests, fixtures)
3. Set the working directory to output/level-{N}/
4. Give aider the initial prompt with full instructions
5. Aider runs autonomously (yes-always mode from .aider.conf.yml)

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`
