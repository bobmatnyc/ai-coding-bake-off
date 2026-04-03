# Evaluation Framework

## Overview

Solutions are evaluated through two mechanisms:

1. **Automated evaluation** --- test suites, code quality tools, coverage analysis
2. **Cross-agent review** --- AI agents evaluate each other's solutions using standardized rubrics

## Automated Evaluation

```bash
# Run all test suites against all agent solutions
python evaluation/automated/run_tests.py

# Run code quality checks
python evaluation/automated/code_quality.py

# Run coverage analysis
python evaluation/automated/coverage_check.py

# Collect timing metrics from metadata.json files
python evaluation/automated/metrics.py
```

## Cross-Agent Review

Each agent reviews two other agents' solutions (assigned randomly to avoid bias). Reviews use the standardized prompt and rubric.

See:
- `cross_review/review_prompt.md` --- The prompt given to reviewing agents
- `cross_review/rubric_template.md` --- Scoring template

## Results

All results are written to `results/`. The `generate_report.py` script aggregates them into a comparison report.
