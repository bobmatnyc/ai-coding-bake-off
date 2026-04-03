FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir "fastapi>=0.111.0" "uvicorn[standard]>=0.29.0" \
    "httpx>=0.27.0" "apscheduler>=3.10.0" "pydantic>=2.7.0"

# Copy application code
COPY weather_alerter/ ./weather_alerter/

# Create directory for SQLite database
RUN mkdir -p /data

ENV DATABASE_PATH=/data/weather.db
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "weather_alerter.app:app", "--host", "0.0.0.0", "--port", "8000"]
