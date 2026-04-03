# Harnesses

Each subdirectory is a self-contained workspace for one AI coding agent. A harness includes everything the agent needs to compete and a place for its output.

## Structure

```
harnesses/
├── {agent-name}/
│   ├── README.md          # Agent profile, how to reproduce
│   ├── instructions/      # Everything the agent needs to know
│   │   ├── CLAUDE.md      # (or .cursorrules, AGENTS.md, etc.)
│   │   └── setup.md       # How to configure and run this agent
│   └── output/            # Where solutions go
│       ├── level-1/
│       │   └── metadata.json
│       ├── level-2/
│       ├── level-3/
│       ├── level-4/
│       └── level-5/
```

## Harnesses

| Directory | Agent | Instruction File | Description |
|-----------|-------|-----------------|-------------|
| `claude-mpm/` | Claude MPM | `CLAUDE.md` + `.claude-mpm/` | Multi-agent orchestration via PM + specialist agents |
| `claude-code/` | Claude Code | `CLAUDE.md` | Anthropic's CLI agent with tool use |
| `cursor/` | Cursor | `.cursorrules` | IDE-integrated AI with Composer and multi-file editing |
| `codex/` | Codex | `AGENTS.md` | OpenAI's CLI agent with sandboxed execution |
| `gemini/` | Gemini CLI | `GEMINI.md` | Google's CLI agent with Gemini 2.5 Pro |
| `anti-gravity/` | Anti-Gravity | `setup.md` | Agentic VS Code extension |
| `augment/` | Augment Code | `setup.md` | Agentic IDE extension (scored 83.1% in Round 1) |
| `qwen-aider/` | Qwen + Aider | `aider.conf.yml` | Local Qwen 3 model via Aider |
| `deepseek-aider/` | DeepSeek + Aider | `aider.conf.yml` | Local DeepSeek V3 model via Aider |

## Rules

- Each agent works independently
- Agents must not view other harnesses' output directories during competition
- Cross-review happens only after all agents have completed their solutions
- Each agent reads the same prompt for a given level

## Adding a New Harness

```bash
./scripts/setup_agent_workspace.sh <agent-name>
```

This creates the full `instructions/` + `output/` structure with metadata templates.
