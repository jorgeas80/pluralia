FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install test dependencies
COPY tests/requirements.txt /tmp/test-requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/test-requirements.txt

# Install API dependencies
COPY services/api/requirements.txt /tmp/api-requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/api-requirements.txt

# Install ingest dependencies
COPY services/ingest/requirements.txt /tmp/ingest-requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/ingest-requirements.txt

# Copy shared domain library
COPY libs /app/libs

# Copy services
COPY services /app/services

# Copy tests
COPY tests /app/tests
COPY pytest.ini /app/pytest.ini

# Set PYTHONPATH to include libs
ENV PYTHONPATH=/app

# Default command runs all tests
CMD ["pytest", "-v"]

