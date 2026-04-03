# OpenAI Codex Harness Setup

## Prerequisites

- OpenAI Codex CLI
- Python 3.12+

## Configuration

1. `cd` to project root
2. `AGENTS.md` in `instructions/` provides Codex-specific instructions

## Running a Challenge

```bash
cd ~/Projects/ai-coding-bake-off
codex "Read prompts/level-1-prompt.md and solve the challenge. Put solution in harnesses/codex/output/level-1/"
```

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install OpenAI Codex CLI
3. From the project root, run the codex command with the prompt
4. Results appear in `harnesses/codex/output/`
