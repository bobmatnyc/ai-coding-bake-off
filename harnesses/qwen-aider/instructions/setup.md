# Qwen + Aider Harness Setup

## Prerequisites

- Python 3.12+
- `pip install aider-chat`
- Ollama with Qwen 3 model pulled: `ollama pull qwen3`

## Configuration

1. Copy `aider.conf.yml` to the working directory or pass flags directly
2. Aider runs in architect mode with Qwen 3 via Ollama

## Running a Challenge

```bash
cd harnesses/qwen-aider/output/level-1
aider --config ../../instructions/aider.conf.yml \
  --message "Read ../../../../prompts/level-1-prompt.md and ../../../../challenges/level-1-table-formatter/PROBLEM.md. Build the solution here."
```

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install aider-chat and Ollama with Qwen 3
3. Run aider from the output directory with the config
4. Results appear in `harnesses/qwen-aider/output/`
