# Agent Workspaces

Each subdirectory is a workspace for one AI coding agent. Solutions for each challenge level live under `{agent-name}/level-{N}/`.

## Agents

| Directory | Agent | Description |
|-----------|-------|-------------|
| `cursor/` | Cursor | IDE-integrated AI with Composer and multi-file editing |
| `claude-code/` | Claude Code | Anthropic's CLI agent with tool use |
| `claude-mpm/` | Claude MPM | Multi-agent orchestration via PM + specialist agents |
| `codex/` | Codex | OpenAI's CLI agent with sandboxed execution |
| `gemini/` | Gemini CLI | Google's CLI agent with Gemini 2.5 Pro |
| `anti-gravity/` | Anti-Gravity | Agentic VS Code extension |
| `qwen-aider/` | Qwen + Aider | Local Qwen 3 model via Aider |
| `deepseek-aider/` | DeepSeek + Aider | Local DeepSeek V3 model via Aider |
| `augment/` | Augment Code | Agentic IDE extension (scored 83.1% in Round 1) |

## Workspace Structure

Each agent's workspace follows this pattern:

```
{agent-name}/
├── README.md              # Agent profile, version, configuration
├── level-1/               # Level 1 solution
│   ├── metadata.json      # Timing and token metrics
│   └── (solution files)
├── level-2/               # Level 2 solution
│   ├── metadata.json
│   └── (solution files)
├── level-3/
├── level-4/
└── level-5/
```

## Rules

- Each agent works independently
- Agents must not view other agents' solutions during the competition phase
- Cross-review happens only after all agents have completed their solutions
- Each agent reads the same prompt for a given level
