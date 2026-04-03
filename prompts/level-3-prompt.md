# Level 3 Challenge: Weather Alerting Service

## Your Task

Read the problem description at `challenges/level-3-weather-alerter/PROBLEM.md` and build a complete solution.

## Workspace Setup

Create your solution in:
```
harnesses/{your-agent-name}/output/level-3/
```

For example:
- Claude MPM -> `harnesses/claude-mpm/output/level-3/`
- Claude Code -> `harnesses/claude-code/output/level-3/`
- Cursor -> `harnesses/cursor/output/level-3/`

## Time Tracking

Record timing in `harnesses/{your-agent-name}/output/level-3/metadata.json` (use `"agent": "claude-mpm"` when running as Claude MPM).

## Delivery Checklist

- [ ] REST API with all city, threshold, alert, and weather endpoints
- [ ] SQLite database with proper schema
- [ ] Background scheduler for periodic weather checks
- [ ] Alert evaluation logic (threshold comparison)
- [ ] Mock/demo mode for testing without API key
- [ ] Dockerfile and docker-compose.yml
- [ ] All provided tests pass: run `pytest challenges/level-3-weather-alerter/test_suite/ -v`
- [ ] Additional tests (API, alert logic, scheduler)
- [ ] README with setup, API docs, Docker instructions

## Constraints

- **Do NOT look at other harnesses' solutions**
- Target Python 3.12+
- Must support both real API and mock mode
- `docker-compose up` should start the service

## Evaluation Note

Your solution will be evaluated using the rubric at:
`challenges/level-3-weather-alerter/evaluation/rubric.md`

Architecture and Docker support are weighted heavily at this level.
