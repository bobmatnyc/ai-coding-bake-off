# Auggie Harness Setup

## Prerequisites

- IDE with Augment Code extension (VS Code or compatible)
- Python 3.12+

## Configuration

1. Open the project root in your IDE with Augment Code
2. No special instruction file needed --- use the prompt directly

## Running a Challenge

1. Open `prompts/level-{N}-prompt.md`
2. Instruct Auggie: "Read this prompt and solve the challenge. Put your solution in harnesses/auggie/output/level-{N}/"
3. Let the agent work

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Notes from Round 1

Augment Code scored 83.1% in the December 2025 benchmark across 3 small Python tasks. Solid code generation but struggled with edge cases compared to orchestrated systems.

## Reproducing

1. Clone the repository
2. Install IDE with Augment Code extension
3. Open the project and provide the prompt
4. Results appear in `harnesses/auggie/output/`
