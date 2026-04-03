# Level 5 Evaluation Rubric: Team Task Board

## Scoring Dimensions (1-5 scale)

### Correctness (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | All API endpoints work. Auth flow complete. WebSocket functional. Frontend renders. docker-compose up works. |
| 4 | Core functionality works. Minor issues in secondary features. |
| 3 | CRUD works. Auth works. WebSocket or frontend has issues. |
| 2 | Basic CRUD works but auth or real-time broken. |
| 1 | Fundamental issues. Does not start. |

### Code Quality (Weight: 10%)
| Score | Criteria |
|-------|----------|
| 5 | Clean, typed, linted. Consistent patterns across backend and frontend. |
| 4 | Good quality. Mostly typed. Minor issues. |
| 3 | Acceptable. Mixed quality. |
| 2 | Poor quality. |
| 1 | Very poor. |

### Architecture (Weight: 25%)
| Score | Criteria |
|-------|----------|
| 5 | Clear layers (routes, services, models, WebSocket). Clean frontend component structure. DB migrations. Seed data. Configuration management. Architecture decisions documented. |
| 4 | Good structure. Mostly clean separation. |
| 3 | Some structure but coupled modules. |
| 2 | Poor organization. |
| 1 | No architecture. |

### Testing (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Unit tests for services. API integration tests. Auth flow tests. WebSocket tests. Frontend tests. 80%+ coverage. |
| 4 | Good API and service tests. Some frontend tests. |
| 3 | Basic API tests. |
| 2 | Minimal tests. |
| 1 | No additional tests. |

### Error Handling (Weight: 10%)
| Score | Criteria |
|-------|----------|
| 5 | Comprehensive input validation. Auth errors handled. WebSocket disconnection handled. DB errors caught. Rate limiting. |
| 4 | Good validation and error handling. |
| 3 | Basic validation. Some error handling. |
| 2 | Crashes on bad input. |
| 1 | No error handling. |

### Documentation (Weight: 10%)
| Score | Criteria |
|-------|----------|
| 5 | Comprehensive README with architecture decisions. OpenAPI docs at /docs. Setup guide. Environment variables documented. |
| 4 | Good README. API docs available. |
| 3 | Basic README. |
| 2 | Minimal. |
| 1 | None. |

### Bonus: Real-time + Docker + CI (Weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | WebSocket real-time updates work. docker-compose up starts everything. CI runs tests and builds. Multi-stage Docker build. Health checks. |
| 4 | WebSocket works. Docker works. CI present. |
| 3 | Two of three (WebSocket, Docker, CI) work. |
| 2 | One of three works. |
| 1 | None work. |
