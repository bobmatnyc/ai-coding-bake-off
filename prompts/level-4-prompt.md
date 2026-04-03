# Level 4 Challenge: Document Processing Pipeline

## Your Task

Read the problem description at `challenges/level-4-doc-pipeline/PROBLEM.md` and build a complete solution.

## Workspace Setup

Create your solution in:
```
harnesses/{your-agent-name}/output/level-4/
```

For example:
- Claude MPM -> `harnesses/claude-mpm/output/level-4/`
- Claude Code -> `harnesses/claude-code/output/level-4/`
- Codex -> `harnesses/codex/output/level-4/`

## Time Tracking

Record timing in `harnesses/{your-agent-name}/output/level-4/metadata.json` (use `"agent": "claude-mpm"` when running as Claude MPM).

## Delivery Checklist

- [ ] Pipeline with all 5 stages (ingestion, extraction, NLP, indexing, storage)
- [ ] Extensible architecture (new stages without modifying existing code)
- [ ] REST API for documents, search, entities, and stats
- [ ] Admin CLI (reprocess, reindex, stats, watch)
- [ ] Full-text search with relevance ranking
- [ ] Architecture diagram (Mermaid, ASCII, or image)
- [ ] All provided tests pass: run `pytest challenges/level-4-doc-pipeline/test_suite/ -v`
- [ ] Comprehensive tests (per-stage unit tests, integration tests)
- [ ] README documenting architecture decisions

## Constraints

- **Do NOT look at other harnesses' solutions**
- Target Python 3.12+
- NLP can use any library (spaCy, NLTK, regex-based, etc.)
- Must demonstrate extensibility with at least one example custom stage

## Evaluation Note

Your solution will be evaluated using the rubric at:
`challenges/level-4-doc-pipeline/evaluation/rubric.md`

**Architecture is 30% of the score.** This is where design decisions matter most. The evaluators will specifically look at whether new pipeline stages can be added without modifying existing code.
