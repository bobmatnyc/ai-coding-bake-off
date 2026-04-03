# Claude Code Harness Setup

## Prerequisites

- Claude Code CLI (latest)
- Python 3.12+

## Configuration

1. `cd` to `harnesses/claude-code/`
2. The `CLAUDE.md` in `instructions/` provides agent-specific instructions
3. Copy or symlink `instructions/CLAUDE.md` to the working directory if needed

## Running a Challenge

```bash
cd harnesses/claude-code
claude  # launches Claude Code
> solve level 1
```

Or from the project root:

```bash
claude "Read harnesses/claude-code/instructions/CLAUDE.md, then read prompts/level-1-prompt.md and solve the challenge."
```

## Output

- Solutions in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install Claude Code CLI
3. `cd harnesses/claude-code`
4. Launch Claude Code: `claude`
5. Issue: `solve level 1`
6. Results appear in `output/`
