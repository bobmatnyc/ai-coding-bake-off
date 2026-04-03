#!/usr/bin/env bash
set -euo pipefail

LEVEL=${1:?Usage: ./run-level.sh <1-5>}
HARNESS_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$HARNESS_DIR/../.." && pwd)"
OUTPUT_DIR="$HARNESS_DIR/output/level-$LEVEL"

# Source API key
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Map level number to challenge directory
case $LEVEL in
    1) CHALLENGE="level-1-table-formatter" ;;
    2) CHALLENGE="level-2-git-analyzer" ;;
    3) CHALLENGE="level-3-weather-alerter" ;;
    4) CHALLENGE="level-4-doc-pipeline" ;;
    5) CHALLENGE="level-5-task-board" ;;
    *) echo "Invalid level: $LEVEL (must be 1-5)"; exit 1 ;;
esac

CHALLENGE_DIR="$PROJECT_ROOT/challenges/$CHALLENGE"

# Collect fixture files for --read
FIXTURES=""
if [ -d "$CHALLENGE_DIR/test_suite/fixtures" ]; then
    for f in "$CHALLENGE_DIR"/test_suite/fixtures/*; do
        [ -f "$f" ] && FIXTURES="$FIXTURES --read $f"
    done
fi

echo "=== Bake-Off: deepseek-aider solving Level $LEVEL ==="
echo "Challenge: $CHALLENGE"
echo "Output: $OUTPUT_DIR"
echo ""

cd "$OUTPUT_DIR"

# Launch aider with all context pre-loaded
aider \
    --config "$HARNESS_DIR/.aider.conf.yml" \
    --read "$CHALLENGE_DIR/PROBLEM.md" \
    --read "$PROJECT_ROOT/prompts/level-${LEVEL}-prompt.md" \
    --read "$CHALLENGE_DIR/evaluation/rubric.md" \
    --read "$CHALLENGE_DIR/test_suite/test_basic.py" \
    $FIXTURES \
    --message "You are deepseek-aider competing in the AI Coding Bake-Off.

CHALLENGE: $CHALLENGE (Level $LEVEL)

Read the PROBLEM.md file for the full problem description. Read the rubric.md to understand how you'll be scored.

Build a complete Python solution in the current directory. This should be a self-contained project with:
- Working source code
- A README.md with usage instructions
- Tests (in addition to the provided test_basic.py)
- Type hints and docstrings

When done, create a metadata.json with:
{
  \"agent\": \"deepseek-aider\",
  \"level\": $LEVEL,
  \"start_time\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"end_time\": \"UPDATE_WHEN_DONE\",
  \"wall_clock_minutes\": null,
  \"estimated_tokens\": null,
  \"model\": \"deepseek-chat-v3.1\",
  \"notes\": \"\"
}

The provided test suite is at: $CHALLENGE_DIR/test_suite/test_basic.py
Run it with: python3 -m pytest $CHALLENGE_DIR/test_suite/test_basic.py -v

Start building the solution now."
