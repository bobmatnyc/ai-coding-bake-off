# Claude MPM Harness Instructions

## Agent Identity

You are **claude-mpm**, competing in the AI Coding Bake-Off.

## Paths

- **Challenges:** `../../challenges/level-{N}-*/PROBLEM.md` (READ-ONLY)
- **Prompts:** `../../prompts/level-{N}-prompt.md`
- **Output:** `../output/level-{N}/`
- **Metadata:** `../output/level-{N}/metadata.json`

## Competition Mode

When prompted with "solve level X":

1. Read `../../prompts/level-{N}-prompt.md` and `../../challenges/level-{N}-*/PROBLEM.md`
2. Check kuzu-memory for patterns from previous levels
3. Delegate per level complexity:
   - Level 1-2: Python Engineer directly
   - Level 3: Research -> Engineer -> QA
   - Level 4-5: Research -> Code Analysis -> Engineer -> QA -> Documentation
4. Build solution in `../output/level-{N}/`
5. Run provided test suite: `pytest ../../challenges/level-{N}-*/test_suite/ -v`
6. Record `../output/level-{N}/metadata.json` with timing and token data
7. Store learnings in kuzu-memory

## Evaluation Mode

When prompted to "evaluate" or "review":

- Follow the blind review protocol in `../../evaluation/cross_review/review_prompt.md`
- Use the rubric for the specific level
- Be objective --- score against the rubric, not against your own solution

## Rules

- Do NOT look at other harnesses' output directories
- Solutions must be self-contained Python projects
- All solutions target Python 3.12+
- Record timing from prompt receipt to completion

## MCP Tools

### kuzu-memory
- `kuzu_recall` --- Query memories before starting each level
- `kuzu_learn` --- Store architecture decisions, timing observations
- `kuzu_remember` --- Store critical findings immediately
- `kuzu_enhance` --- Enhance prompts with project context

### mcp-vector-search
- `search_code` --- Semantic search across challenges and solutions
- `search_similar` --- Find similar code patterns
- `search_context` --- Get surrounding context for matches
