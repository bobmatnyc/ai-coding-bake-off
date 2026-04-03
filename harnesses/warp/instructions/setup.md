# Warp Harness Setup

## Prerequisites

- Warp terminal (latest version)
- Warp AI Agent mode enabled
- Python 3.12+

## Configuration

1. Open Warp terminal
2. Navigate to project root: `cd ~/Projects/ai-coding-bake-off`
3. Enter Agent mode (# key or type `/agent`)

## Running a Challenge

1. In Warp Agent mode, paste:
   "Read prompts/level-{N}-prompt.md and challenges/level-{N}-*/PROBLEM.md. Solve the challenge and put your solution in harnesses/warp/output/level-{N}/"
2. Let the agent work
3. Fill in metadata.json when complete

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install Warp terminal
3. Enter Agent mode and provide the prompt
4. Results appear in `harnesses/warp/output/`
