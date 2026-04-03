# Level 4 Evaluation Rubric: Document Processing Pipeline

## Scoring Dimensions (1-5 scale)

### Correctness (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | All stages work. Search returns relevant results. API functional. CLI works. |
| 4 | Core pipeline works. Search mostly accurate. Minor issues. |
| 3 | Pipeline runs but some stages produce poor results. |
| 2 | Some stages work in isolation but pipeline integration broken. |
| 1 | Pipeline fundamentally broken. |

### Code Quality (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Clean, well-typed code. Consistent patterns. Passes strict linting. |
| 4 | Good quality. Typed public API. Minor issues. |
| 3 | Acceptable. Mixed quality across modules. |
| 2 | Poor quality. Hard to read. |
| 1 | Very poor. |

### Architecture (Weight: 30%)
| Score | Criteria |
|-------|----------|
| 5 | True plugin system. New stages added without modifying existing code. Clean interfaces. Dependency management between stages. Architecture diagram included. |
| 4 | Good extensibility. Clear stage interfaces. Some coupling. |
| 3 | Stages exist but adding new ones requires modifying core pipeline. |
| 2 | Monolithic. Pipeline stages tightly coupled. |
| 1 | No pipeline architecture. Everything in one function. |

### Testing (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Unit tests per stage. Integration tests for full pipeline. Search tests. API tests. Mocked NLP for speed. |
| 4 | Good coverage of stages and API. |
| 3 | Basic tests. Missing integration tests. |
| 2 | Minimal tests. |
| 1 | No additional tests. |

### Error Handling (Weight: 10%)
| Score | Criteria |
|-------|----------|
| 5 | Stage failures isolated. Documents marked with error status. Retry logic. Detailed error logging. |
| 4 | Good error isolation. Documents tracked even on failure. |
| 3 | Some error handling but failures cascade. |
| 2 | Crashes on bad documents. |
| 1 | No error handling. |

### Documentation (Weight: 10%)
| Score | Criteria |
|-------|----------|
| 5 | Architecture decisions document. README with setup, usage, extending. API docs. Diagram. |
| 4 | Good README. Architecture explained. |
| 3 | Basic README. |
| 2 | Minimal. |
| 1 | None. |

### Bonus: Extensibility Demo (Weight: 5%)
| Score | Criteria |
|-------|----------|
| 5 | Includes a custom example stage (e.g., sentiment analysis) demonstrating the plugin system. |
| 4 | Plugin system documented with instructions for adding stages. |
| 3 | Extension points exist but undocumented. |
| 2 | Claims extensibility but no evidence. |
| 1 | N/A. |
