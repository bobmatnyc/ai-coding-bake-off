#!/usr/bin/env bash
# Setup an agent workspace with subdirectories for each challenge level.
#
# Usage:
#   ./scripts/setup_agent_workspace.sh <agent-name>
#
# Example:
#   ./scripts/setup_agent_workspace.sh claude-code

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <agent-name>"
    echo ""
    echo "Available agents: cursor, claude-code, claude-mpm, codex, gemini, anti-gravity, qwen-aider, deepseek-aider"
    echo "Or provide a custom agent name."
    exit 1
fi

AGENT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
AGENT_DIR="$PROJECT_ROOT/agents/$AGENT_NAME"

echo "Setting up workspace for agent: $AGENT_NAME"
echo "Directory: $AGENT_DIR"

# Create level directories
for level in 1 2 3 4 5; do
    level_dir="$AGENT_DIR/level-$level"
    mkdir -p "$level_dir"

    # Create metadata.json template
    if [ ! -f "$level_dir/metadata.json" ]; then
        cat > "$level_dir/metadata.json" << EOF
{
  "agent": "$AGENT_NAME",
  "level": $level,
  "start_time": null,
  "end_time": null,
  "wall_clock_minutes": null,
  "estimated_tokens": null,
  "notes": ""
}
EOF
    fi

    echo "  Created level-$level/ with metadata.json"
done

# Create agent README if it doesn't exist
if [ ! -f "$AGENT_DIR/README.md" ]; then
    cat > "$AGENT_DIR/README.md" << EOF
# $AGENT_NAME

## Agent Profile

- **Name:** $AGENT_NAME
- **Version:** (fill in)
- **Configuration:** (describe setup)

## How to Reproduce

1. (Describe how to set up this agent)
2. (Describe how to give it the prompt)
3. (Describe any special configuration)

## Solutions

| Level | Status | Time | Notes |
|-------|--------|------|-------|
| 1 | Not started | - | - |
| 2 | Not started | - | - |
| 3 | Not started | - | - |
| 4 | Not started | - | - |
| 5 | Not started | - | - |
EOF
    echo "  Created README.md"
fi

echo ""
echo "Workspace ready. Give the agent the prompt from:"
echo "  prompts/level-1-prompt.md"
echo ""
echo "The agent should create its solution in:"
echo "  agents/$AGENT_NAME/level-1/"
