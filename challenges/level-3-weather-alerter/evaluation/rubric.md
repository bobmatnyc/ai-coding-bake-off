# Level 3 Evaluation Rubric: Weather Alerting Service

## Scoring Dimensions (1-5 scale)

### Correctness (Weight: 20%)
| Score | Criteria |
|-------|----------|
| 5 | All endpoints work correctly. Alert logic accurate. Scheduler runs. Mock mode works. |
| 4 | Core endpoints work. Alert logic correct. Minor issues. |
| 3 | Most endpoints work. Some alert logic issues. |
| 2 | Basic CRUD works but alert system broken. |
| 1 | API mostly non-functional. |

### Code Quality (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Clean code. Type hints. Passes linting. Pydantic models for validation. |
| 4 | Good quality. Mostly typed. Minor issues. |
| 3 | Acceptable. Some type hints. |
| 2 | Messy. No validation. |
| 1 | Very poor quality. |

### Architecture (Weight: 20%)
| Score | Criteria |
|-------|----------|
| 5 | Clean layers (routes, services, models, alerts). Dependency injection. Configurable. |
| 4 | Good separation. Clear boundaries. |
| 3 | Some separation but coupled. |
| 2 | Everything mixed together. |
| 1 | No structure. |

### Testing (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Tests for all endpoints, alert logic, scheduler, edge cases. Mocked external API. |
| 4 | Good API tests and alert logic tests. |
| 3 | Basic endpoint tests only. |
| 2 | Minimal tests. |
| 1 | No additional tests. |

### Error Handling (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Handles API failures, invalid input, missing cities, DB errors. Retries on network failure. |
| 4 | Handles common errors. Validates input. |
| 3 | Some validation and error handling. |
| 2 | Crashes on bad input. |
| 1 | No error handling. |

### Documentation (Weight: 5%)
| Score | Criteria |
|-------|----------|
| 5 | Complete README with API docs, setup, Docker instructions, examples. |
| 4 | Good README. API endpoints documented. |
| 3 | Basic README. |
| 2 | Minimal documentation. |
| 1 | No documentation. |

### Bonus: Docker (Weight: 10%)
| Score | Criteria |
|-------|----------|
| 5 | Works with `docker-compose up`. Multi-stage build. Health check. Volume mounts. .env support. |
| 4 | Docker works. Some best practices. |
| 3 | Dockerfile present but issues. |
| 2 | Incomplete Docker setup. |
| 1 | No Docker. |
