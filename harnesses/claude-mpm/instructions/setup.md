# Claude MPM Harness Setup

## Prerequisites

- Claude Code CLI with MPM plugin
- kuzu-memory MCP server configured
- mcp-vector-search MCP server configured
- Python 3.12+

## Configuration

1. `cd` to `harnesses/claude-mpm/`
2. The `CLAUDE.md` and `.claude-mpm/` in `instructions/` configure the agent
3. Symlink or copy `instructions/CLAUDE.md` to the working directory if needed

## Running a Challenge

From the project root:

```bash
cd harnesses/claude-mpm
claude  # launches Claude Code with MPM
> solve level 1
```

The agent reads prompts from `prompts/level-{N}-prompt.md`, reads challenge definitions from `challenges/level-{N}-*/PROBLEM.md`, and writes solutions to `harnesses/claude-mpm/output/level-{N}/`.

## Output

- Solutions appear in `output/level-{N}/`
- Metadata in `output/level-{N}/metadata.json`

## Reproducing

1. Clone the repository
2. Install Claude Code CLI with MPM plugin
3. Configure kuzu-memory and mcp-vector-search MCP servers
4. `cd harnesses/claude-mpm`
5. Launch Claude Code: `claude`
6. Issue: `solve level 1` (or any level 1-5)
7. Wait for completion; results appear in `output/`
