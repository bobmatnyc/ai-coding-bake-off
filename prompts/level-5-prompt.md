# Level 5 Challenge: Team Task Board

## Your Task

Read the problem description at `challenges/level-5-task-board/PROBLEM.md` and build a complete solution.

## Workspace Setup

Create your solution in:
```
agents/{your-agent-name}/level-5/
```

For example:
- Claude MPM → `agents/claude-mpm/level-5/`
- Claude Code → `agents/claude-code/level-5/`
- Cursor → `agents/cursor/level-5/`

## Time Tracking

Record timing in `agents/{your-agent-name}/level-5/metadata.json` (use `"agent": "claude-mpm"` when running as Claude MPM).

## Delivery Checklist

- [ ] Backend REST API with all task, board, column, activity endpoints
- [ ] JWT authentication (register, login, refresh, protected routes)
- [ ] WebSocket for real-time task updates
- [ ] PostgreSQL with migrations and seed data
- [ ] Web frontend with Kanban board UI
- [ ] Drag-and-drop (or click-based) task movement
- [ ] Real-time updates on the frontend
- [ ] Docker Compose: `docker-compose up` starts everything
- [ ] GitHub Actions CI workflow
- [ ] OpenAPI/Swagger docs at /docs
- [ ] All provided tests pass: run `pytest challenges/level-5-task-board/test_suite/ -v`
- [ ] Comprehensive test suite (unit, integration, API, WebSocket)
- [ ] README with architecture decisions, setup guide, API overview

## Constraints

- **Do NOT look at other agents' solutions**
- Target Python 3.12+
- The system must start with `docker-compose up`
- Must include database migrations (not just CREATE TABLE)
- Must include seed data

## Evaluation Note

Your solution will be evaluated using the rubric at:
`challenges/level-5-task-board/evaluation/rubric.md`

**This is the ultimate test.** Architecture (25%) and Bonus (15%) together make up 40% of the score. The evaluators will test whether `docker-compose up` works, whether real-time updates function, and whether the CI pipeline is valid.

This challenge is designed to be very difficult. Partial completion is expected and will be scored accordingly.
