# Gemini CLI Harness Setup

## Prerequisites

- Gemini CLI (latest)
- Python 3.12+

## Configuration

1. `cd` to project root
2. `GEMINI.md` in `instructions/` provides Gemini-specific instructions

## Running a Challenge

```bash
cd ~/Projects/ai-coding-bake-off
gemini "Read prompts/level-1-prompt.md and solve the challenge. Put solution in harnesses/gemini/output/level-1/"
```

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install Gemini CLI
3. From the project root, run the gemini command with the prompt
4. Results appear in `harnesses/gemini/output/`
