FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY services/ingest/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

# Copy shared domain library
COPY libs /app/libs

# Copy the ingest service
COPY services/ingest /app/services/ingest

# Set PYTHONPATH to include libs
ENV PYTHONPATH=/app

# No default CMD - runs manually when needed
# docker-compose run --rm pluralia-ingest python -m services.ingest.src.main

