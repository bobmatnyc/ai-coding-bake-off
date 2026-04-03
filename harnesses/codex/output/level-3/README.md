# Weather Alerting Service

Level 3 solution for the AI coding bake-off. The service exposes a FastAPI REST API, stores configuration and alert history in SQLite, supports a mock weather mode for local testing, and can run periodic threshold checks in the background.

## Features

- CRUD API for monitored cities and thresholds
- Alert history endpoint with pagination and filtering
- Current weather endpoint with real OpenWeatherMap support or bundled mock mode
- SQLite persistence via SQLAlchemy
- Background scheduler for periodic alert checks
- Dockerfile and `docker-compose.yml`

## Configuration

Environment variables:

- `OPENWEATHERMAP_API_KEY`: API key for live weather calls
- `WEATHER_ALERTER_MOCK_MODE`: `true` or `false`; defaults to `true` when no API key is present
- `WEATHER_ALERTER_DB_URL`: SQLAlchemy database URL
- `WEATHER_ALERTER_POLL_SECONDS`: scheduler interval in seconds, default `300`

## Running Locally

From this directory:

```bash
python3 -m weather_alerter
```

The API will be available at `http://localhost:8000`.

## Example API Usage

```bash
curl http://localhost:8000/api/health

curl -X POST http://localhost:8000/api/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194}'

curl -X POST http://localhost:8000/api/cities/1/thresholds \
  -H "Content-Type: application/json" \
  -d '{"metric": "temperature", "operator": "gt", "value": 35.0}'

curl http://localhost:8000/api/weather/1
curl http://localhost:8000/api/alerts
```

## Docker

```bash
docker-compose up --build
```

This starts the API on port `8000` and persists the SQLite database in a named volume.

## Tests

Run the local test suite:

```bash
python3 -m pytest tests -v
```

Run the provided benchmark tests from the repository root:

```bash
cd ../../..
python3 -m pytest challenges/level-3-weather-alerter/test_suite -v
```
