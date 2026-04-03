# Level 2 Evaluation Rubric: Git Log Analyzer

## Scoring Dimensions (1-5 scale)

### Correctness (Weight: 25%)

| Score | Criteria |
|-------|----------|
| 5 | All tests pass. Metrics are accurate. Both output formats work. Handles real repos. |
| 4 | All tests pass. Minor metric inaccuracies. |
| 3 | Most tests pass. Some metrics incorrect. |
| 2 | Basic parsing works but metrics have errors. |
| 1 | Parsing fails or metrics fundamentally wrong. |

### Code Quality (Weight: 20%)

| Score | Criteria |
|-------|----------|
| 5 | Clean separation into modules. Type hints throughout. Passes ruff/mypy. Idiomatic. |
| 4 | Good structure. Type hints on public API. Minor issues. |
| 3 | Functional but some large functions. Partial type hints. |
| 2 | Monolithic. No type hints. Style issues. |
| 1 | Difficult to read or maintain. |

### Architecture (Weight: 15%)

| Score | Criteria |
|-------|----------|
| 5 | Clean parser/metrics/reporter separation. Easy to extend with new metrics. Proper src layout. |
| 4 | Good separation. Mostly follows project structure spec. |
| 3 | Some separation but coupled modules. |
| 2 | Poor organization. Logic mixed across files. |
| 1 | Everything in one file. |

### Testing (Weight: 15%)

| Score | Criteria |
|-------|----------|
| 5 | Comprehensive tests for parser, metrics, and CLI. Uses fixtures. Tests edge cases. |
| 4 | Good test coverage. Tests main paths. |
| 3 | Basic tests. Misses edge cases. |
| 2 | Minimal tests. |
| 1 | No additional tests. |

### Error Handling (Weight: 10%)

| Score | Criteria |
|-------|----------|
| 5 | Handles non-git dirs, empty repos, binary files, encoding issues gracefully. |
| 4 | Handles common error cases. |
| 3 | Some error handling. |
| 2 | Crashes on edge cases. |
| 1 | No error handling. |

### Documentation (Weight: 10%)

| Score | Criteria |
|-------|----------|
| 5 | Complete README with installation, usage, examples, sample output. Module docstrings. |
| 4 | Good README. Most modules documented. |
| 3 | Basic README. Some docstrings. |
| 2 | Minimal documentation. |
| 1 | No documentation. |

### Bonus: Packaging (Weight: 5%)

| Score | Criteria |
|-------|----------|
| 5 | Proper pyproject.toml with entry points. Installable via pip. Version pinning. |
| 4 | pyproject.toml present. Mostly correct. |
| 3 | Basic setup but incomplete. |
| 2 | No packaging. |
| 1 | N/A |
