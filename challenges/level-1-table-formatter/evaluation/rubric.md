# Level 1 Evaluation Rubric: Markdown Table Formatter

## Scoring Dimensions (1-5 scale)

### Correctness (Weight: 30%)

| Score | Criteria |
|-------|----------|
| 5 | All provided tests pass. Handles all edge cases perfectly. Output is valid Markdown. |
| 4 | All provided tests pass. Minor formatting issues on edge cases. |
| 3 | Most tests pass (80%+). Some edge cases mishandled. |
| 2 | Core functionality works but multiple test failures. |
| 1 | Fundamental issues. Most tests fail. |

### Code Quality (Weight: 25%)

| Score | Criteria |
|-------|----------|
| 5 | Clean, idiomatic Python. Type hints throughout. Passes ruff and mypy strict. Well-structured. |
| 4 | Good code quality. Type hints on public API. Minor linting issues. |
| 3 | Acceptable code. Some type hints. Some linting issues. |
| 2 | Messy code. No type hints. Significant style issues. |
| 1 | Difficult to read. No structure or conventions. |

### Architecture (Weight: 5%)

| Score | Criteria |
|-------|----------|
| 5 | Clean separation of CLI, parsing, and formatting. Reusable as a library. |
| 4 | Reasonable structure. Mostly separates concerns. |
| 3 | Functional but monolithic. Everything in one function. |
| 2 | Poor organization. Hard to extend. |
| 1 | No structure whatsoever. |

### Testing (Weight: 20%)

| Score | Criteria |
|-------|----------|
| 5 | 10+ additional tests. Tests edge cases, error paths, and CLI flags. Good coverage. |
| 4 | 5-9 additional tests. Covers major functionality. |
| 3 | Minimal additional tests (1-4). Covers basic cases only. |
| 2 | No additional tests beyond provided suite. |
| 1 | Tests are broken or absent. |

### Error Handling (Weight: 15%)

| Score | Criteria |
|-------|----------|
| 5 | Graceful handling of all error cases. Helpful error messages. Non-zero exit codes. |
| 4 | Handles common errors (missing file, bad CSV). Good messages. |
| 3 | Basic error handling. Some crashes on bad input. |
| 2 | Minimal error handling. Crashes on edge cases. |
| 1 | No error handling. Stack traces to user. |

### Documentation (Weight: 5%)

| Score | Criteria |
|-------|----------|
| 5 | Complete README with examples. Docstrings on all public functions. |
| 4 | Good README. Most functions documented. |
| 3 | Basic README. Some docstrings. |
| 2 | Minimal documentation. |
| 1 | No documentation. |

## Bonus Points (up to +0.5)

- Supports additional output formats (HTML, RST)
- Configurable via a config file
- Colorized terminal output
- Progress bar for large files
