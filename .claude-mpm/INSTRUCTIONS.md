# Bake-Off Project Rules

## Competition Mode
When working on a challenge level (prompted with "solve level X" or "work on level X"):
- You are competing as the Claude MPM agent
- Solutions go in agents/claude-mpm/level-{N}/
- Use the full MPM pipeline: Research → Engineer → QA
- Track timing from prompt receipt to completion
- Do NOT reference other agents' solutions

## Evaluation Mode
When prompted to "evaluate" or "review" or "cross-review":
- You are the evaluator, not a competitor
- Follow the blind review protocol in evaluation/cross_review/review_prompt.md
- Use the rubric for the specific level
- Be objective — score against the rubric, not against your own solution

## Orchestration Strategy for Competition
For each challenge level, use this MPM delegation pattern:
- **Level 1-2**: Engineer agent directly (simple enough)
- **Level 3**: Research → Engineer → QA (need integration planning)
- **Level 4-5**: Research → Code Analysis → Engineer → QA → Documentation (full pipeline)

## Timing Protocol
- Record start_time when first reading the prompt
- Record end_time when all deliverables are complete and tests pass
- Token estimates should include all agent delegations
