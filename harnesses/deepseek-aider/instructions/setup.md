# DeepSeek + Aider Harness Setup

## Prerequisites

- Python 3.12+
- `pip install aider-chat`
- Ollama with DeepSeek V3 model pulled: `ollama pull deepseek-v3`

## Configuration

1. Copy `aider.conf.yml` to the working directory or pass flags directly
2. Aider runs in architect mode with DeepSeek V3 via Ollama

## Running a Challenge

```bash
cd harnesses/deepseek-aider/output/level-1
aider --config ../../instructions/aider.conf.yml \
  --message "Read ../../../../prompts/level-1-prompt.md and ../../../../challenges/level-1-table-formatter/PROBLEM.md. Build the solution here."
```

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install aider-chat and Ollama with DeepSeek V3
3. Run aider from the output directory with the config
4. Results appear in `harnesses/deepseek-aider/output/`
