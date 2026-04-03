FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY doc_pipeline/ doc_pipeline/

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Default command: run the API server
CMD ["uvicorn", "doc_pipeline.app:app", "--host", "0.0.0.0", "--port", "8000"]
