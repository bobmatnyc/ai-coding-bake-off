# Level 3: Weather Alerting Service

**Time Budget:** ~2 hours  
**Difficulty:** Medium  
**Focus:** REST API, external API integration, SQLite, background scheduling, Docker

## Problem Statement

Build a weather monitoring service that checks current conditions for configured cities and triggers alerts when thresholds are exceeded. The service exposes a REST API for configuration and provides persistent storage for alert history.

## Requirements

### External API Integration

Use the OpenWeatherMap API (free tier) for weather data:
- Base URL: `https://api.openweathermap.org/data/2.5/weather`
- API key passed via environment variable `OPENWEATHERMAP_API_KEY`
- For testing without an API key, the service should support a mock/demo mode using fixture data

### Data Model

**City Configuration**:
```
- id: integer (auto-increment)
- name: string (e.g., "San Francisco")
- latitude: float
- longitude: float
- enabled: boolean (default true)
- created_at: datetime
```

**Alert Threshold**:
```
- id: integer (auto-increment)
- city_id: integer (FK to cities)
- metric: string (one of: "temperature", "humidity", "wind_speed")
- operator: string (one of: "gt", "lt", "gte", "lte")
- value: float
- enabled: boolean (default true)
```

**Alert Log**:
```
- id: integer (auto-increment)
- city_id: integer (FK to cities)
- threshold_id: integer (FK to thresholds)
- triggered_at: datetime
- metric_value: float
- message: string
```

### REST API Endpoints

```
POST   /api/cities                    # Add a city to monitor
GET    /api/cities                    # List all monitored cities
GET    /api/cities/{id}               # Get city details
DELETE /api/cities/{id}               # Remove a city
PATCH  /api/cities/{id}               # Update city (enable/disable)

POST   /api/cities/{id}/thresholds    # Add alert threshold for a city
GET    /api/cities/{id}/thresholds    # List thresholds for a city
DELETE /api/thresholds/{id}           # Remove a threshold

GET    /api/alerts                    # List recent alerts (with pagination)
GET    /api/alerts?city_id=1          # Filter alerts by city

GET    /api/weather/{city_id}         # Get current weather for a city (live fetch)

GET    /api/health                    # Health check endpoint
```

### Background Scheduler

- Check weather for all enabled cities on a configurable interval (default: every 5 minutes)
- Compare current values against configured thresholds
- Log alerts to the database when thresholds are exceeded
- Print alert messages to stdout

### Docker Support

Provide a `docker-compose.yml` that starts the service with:
```bash
docker-compose up
```

The compose file should:
- Build the application container
- Expose the API on port 8000
- Mount a volume for the SQLite database
- Accept the API key via environment variable

## Example Workflow

```bash
# Start the service
docker-compose up -d

# Add a city
curl -X POST http://localhost:8000/api/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194}'

# Add a temperature threshold (alert if temp > 35°C)
curl -X POST http://localhost:8000/api/cities/1/thresholds \
  -H "Content-Type: application/json" \
  -d '{"metric": "temperature", "operator": "gt", "value": 35.0}'

# Check current weather
curl http://localhost:8000/api/weather/1

# View alerts
curl http://localhost:8000/api/alerts
```

## Deliverables

1. REST API application (FastAPI or Flask)
2. SQLite database with schema migration/initialization
3. Background scheduler for weather checks
4. Dockerfile and docker-compose.yml
5. Tests covering API endpoints and alert logic
6. README with setup and usage instructions

## Open Decisions (Agent's Choice)

- Web framework (FastAPI, Flask, or other)
- ORM vs. raw SQL (SQLAlchemy, Tortoise, raw sqlite3)
- Scheduler library (APScheduler, schedule, celery-beat, asyncio tasks)
- How to handle the mock/demo mode for testing without API key
- Request validation approach
- Logging strategy
- Database migration approach

## Evaluation Criteria

See `evaluation/rubric.md` for the full scoring rubric. Key weights for this level:

- **Correctness**: 20%
- **Code Quality**: 15%
- **Architecture**: 20%
- **Testing**: 15%
- **Error Handling**: 15%
- **Documentation**: 5%
- **Bonus (Docker)**: 10%
