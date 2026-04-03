# Bake-Off Workflow

## Competition Workflow (per level)

### Phase 1: Understand
- Read prompts/level-{N}-prompt.md
- Read challenges/level-{N}-*/PROBLEM.md
- Read challenges/level-{N}-*/evaluation/rubric.md (know what you're scored on)

### Phase 2: Plan (Level 3+ only)
- Research agent analyzes problem requirements
- Identify architecture decisions, external dependencies
- Plan component structure

### Phase 3: Implement
- Engineer creates solution in agents/claude-mpm/level-{N}/
- Iterative: write code → run tests → fix → repeat
- Include README.md, type hints, docstrings

### Phase 4: Test
- Run provided test suite: pytest challenges/level-{N}-*/test_suite/
- Run agent's own tests: pytest agents/claude-mpm/level-{N}/tests/
- Check coverage: pytest --cov agents/claude-mpm/level-{N}/

### Phase 5: Finalize
- Fill metadata.json with timing/token data
- Verify delivery checklist from prompt
- Commit solution

## Evaluation Workflow

### Phase 1: Automated Scoring
- Run all evaluation/automated/ scripts
- Collect results in evaluation/results/

### Phase 2: Cross-Review
- Anonymize solutions (assign random IDs)
- Review each solution against rubric
- Write structured reviews

### Phase 3: Report
- Aggregate scores
- Generate comparison report
- Draft article sections
