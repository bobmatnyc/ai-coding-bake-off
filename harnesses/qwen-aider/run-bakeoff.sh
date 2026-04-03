#!/usr/bin/env bash
set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== AI Coding Bake-Off: qwen-aider ==="
echo "Running all 5 levels sequentially"
echo ""

for level in 1 2 3 4 5; do
    echo ""
    echo "=========================================="
    echo "  Level $level"
    echo "=========================================="
    echo ""
    "$HARNESS_DIR/run-level.sh" "$level"
done

echo ""
echo "=== Bake-Off complete for qwen-aider ==="
echo "Solutions in: $HARNESS_DIR/output/"
