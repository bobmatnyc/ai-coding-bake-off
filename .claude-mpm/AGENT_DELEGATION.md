# Bake-Off Agent Delegation

## Competition Mode Routing

| Challenge Level | Primary Agent | Pipeline |
|----------------|---------------|----------|
| Level 1-2 | Python Engineer | Engineer only |
| Level 3 | Python Engineer + QA | Research → Engineer → QA |
| Level 4-5 | Python Engineer + QA | Research → Code Analysis → Engineer → QA → Docs |

## Evaluation Mode Routing

| Task | Agent | Notes |
|------|-------|-------|
| Automated metrics | Local Ops | Run evaluation scripts |
| Cross-review | Research + Engineer | Research analyzes code, Engineer reviews architecture |
| Report generation | Local Ops | Run report scripts |

## Key Constraints
- Python Engineer for ALL solution code (this is a Python-only benchmark)
- QA for test verification (run pytest, check coverage)
- Local Ops for script execution (evaluation automation)
- Documentation Agent for publication materials (article draft)
