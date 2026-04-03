# Prompts

Standardized prompts for each challenge level. Each agent receives the same prompt for a given level.

## How to Use

1. Give the agent the appropriate `level-X-prompt.md` file
2. The agent reads it and follows the instructions
3. The agent works in its designated workspace under `harnesses/{agent-name}/output/`

## Prompt Structure

Each prompt includes:
1. Problem reference (points to `challenges/level-X-*/PROBLEM.md`)
2. Workspace setup instructions
3. Time tracking requirements
4. Delivery checklist
5. Constraint: do not view other harnesses' solutions
6. Evaluation note
