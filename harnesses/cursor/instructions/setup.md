# Cursor Harness Setup

## Prerequisites

- Cursor IDE (latest)
- Python 3.12+

## Configuration

1. Open the project root in Cursor
2. The `.cursorrules` in `instructions/` provides Cursor-specific rules
3. Copy `.cursorrules` to project root, or Cursor will read it from here

## Running a Challenge

1. Open `prompts/level-{N}-prompt.md` in Cursor
2. Paste into Cursor chat: "Read the prompt in this file and solve the challenge. Put your solution in harnesses/cursor/output/level-{N}/"
3. Let Cursor work

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install Cursor IDE
3. Open the project root in Cursor
4. Copy `.cursorrules` from `harnesses/cursor/instructions/` to project root
5. Open the prompt file and paste the instruction into Cursor chat
6. Results appear in `harnesses/cursor/output/`
