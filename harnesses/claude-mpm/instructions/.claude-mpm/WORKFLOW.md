# Bake-Off Workflows

## One-Line Prompt Workflows

### "solve level {N}" --- Competition Mode
1. PM reads `prompts/level-{N}-prompt.md` and `challenges/level-{N}-*/PROBLEM.md`
2. PM checks kuzu-memory for patterns from previous levels
3. PM delegates per level complexity:
   - Level 1-2: Python Engineer directly
   - Level 3: Research -> Python Engineer -> QA  
   - Level 4-5: Research -> Code Analysis -> Python Engineer -> QA -> Documentation
4. Engineer builds solution in `harnesses/claude-mpm/output/level-{N}/`
5. QA runs provided test suite + agent's tests + coverage
6. PM records metadata.json with timing and token data
7. PM stores learnings in kuzu-memory

### "evaluate level {N}" --- Evaluation Mode
1. PM reads `evaluation/cross_review/review_prompt.md`
2. PM delegates to Local Ops: run automated evaluation scripts
3. PM delegates cross-review to Research (analyze code) + Engineer (review architecture)
4. Results written to `evaluation/results/`

### "evaluate all" --- Full Evaluation
1. Run "evaluate level N" for N=1..5
2. Run `scripts/collect_metrics.py` and `scripts/generate_report.py`
3. Store summary in kuzu-memory

### "run bake-off" --- Full Competition
1. Run "solve level N" for N=1..5 sequentially
2. Run "evaluate all"
3. Generate article draft from `docs/article-outline.md`

---

# Detailed Workflow

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
- Engineer creates solution in harnesses/claude-mpm/output/level-{N}/
- Iterative: write code -> run tests -> fix -> repeat
- Include README.md, type hints, docstrings

### Phase 4: Test
- Run provided test suite: pytest challenges/level-{N}-*/test_suite/
- Run agent's own tests: pytest harnesses/claude-mpm/output/level-{N}/tests/
- Check coverage: pytest --cov harnesses/claude-mpm/output/level-{N}/

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
