#!/usr/bin/env bash
# Setup a harness workspace with instructions/ and output/ subdirectories.
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
    echo "Available agents: cursor, claude-code, claude-mpm, codex, gemini, anti-gravity, auggie, qwen-aider, deepseek-aider, warp"
    echo "Or provide a custom agent name."
    exit 1
fi

AGENT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HARNESS_DIR="$PROJECT_ROOT/harnesses/$AGENT_NAME"

echo "Setting up harness for agent: $AGENT_NAME"
echo "Directory: $HARNESS_DIR"

# Create instructions directory
mkdir -p "$HARNESS_DIR/instructions"

# Create output level directories
for level in 1 2 3 4 5; do
    level_dir="$HARNESS_DIR/output/level-$level"
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

    echo "  Created output/level-$level/ with metadata.json"
done

# Create agent README if it doesn't exist
if [ ! -f "$HARNESS_DIR/README.md" ]; then
    cat > "$HARNESS_DIR/README.md" << EOF
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

# Create setup.md if it doesn't exist
if [ ! -f "$HARNESS_DIR/instructions/setup.md" ]; then
    cat > "$HARNESS_DIR/instructions/setup.md" << EOF
# $AGENT_NAME Harness Setup

## Prerequisites

- Python 3.12+
- (Add agent-specific prerequisites)

## Configuration

1. (Add agent-specific configuration steps)

## Running a Challenge

1. Read the prompt from \`prompts/level-{N}-prompt.md\`
2. Build your solution in \`output/level-{N}/\`

## Output

- Solutions in \`output/level-{N}/\`
- Metadata in \`output/level-{N}/metadata.json\`
EOF
    echo "  Created instructions/setup.md"
fi

echo ""
echo "Harness ready. Give the agent the prompt from:"
echo "  prompts/level-1-prompt.md"
echo ""
echo "The agent should create its solution in:"
echo "  harnesses/$AGENT_NAME/output/level-1/"
