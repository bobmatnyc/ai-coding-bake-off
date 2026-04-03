# Bake-Off Project Rules

## Agent Identity
When this project is run under Claude MPM, the agent name is **claude-mpm**.
All solution output goes to: `harnesses/claude-mpm/output/level-{N}/`
All metadata files: `harnesses/claude-mpm/output/level-{N}/metadata.json`

## Competition Mode
When working on a challenge level (prompted with "solve level X" or "work on level X"):
- You are competing as the Claude MPM agent
- Solutions go in harnesses/claude-mpm/output/level-{N}/
- Use the full MPM pipeline: Research -> Engineer -> QA
- Track timing from prompt receipt to completion
- Do NOT reference other harnesses' solutions

## Evaluation Mode
When prompted to "evaluate" or "review" or "cross-review":
- You are the evaluator, not a competitor
- Follow the blind review protocol in evaluation/cross_review/review_prompt.md
- Use the rubric for the specific level
- Be objective --- score against the rubric, not against your own solution

## Orchestration Strategy for Competition
For each challenge level, use this MPM delegation pattern:
- **Level 1-2**: Engineer agent directly (simple enough)
- **Level 3**: Research -> Engineer -> QA (need integration planning)
- **Level 4-5**: Research -> Code Analysis -> Engineer -> QA -> Documentation (full pipeline)

## Timing Protocol
- Record start_time when first reading the prompt
- Record end_time when all deliverables are complete and tests pass
- Token estimates should include all agent delegations

## MCP Tools Available

### kuzu-memory
- `kuzu_recall` --- Query memories before starting each level (what worked in previous levels)
- `kuzu_learn` --- Store architecture decisions, timing observations, quality patterns
- `kuzu_remember` --- Store critical findings immediately (evaluation scores, blockers)
- `kuzu_enhance` --- Enhance prompts with project context

### mcp-vector-search
- `search_code` --- Semantic search across challenges, solutions, and evaluations
- `search_similar` --- Find similar code patterns across agent solutions
- `search_context` --- Get surrounding context for matches
- `analyze_project` --- Project-wide metrics and analysis

### When to Use
- **Starting a level**: Recall what worked in previous levels, search similar problems
- **During implementation**: Search challenge fixtures and test expectations
- **During evaluation**: Compare solutions semantically, find patterns across agents
- **Writing the article**: Search for interesting findings, recall key metrics
