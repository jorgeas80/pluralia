FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY services/api/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

# Copy shared domain library
COPY libs /app/libs

# Copy the API service
COPY services/api /app/services/api

# Set PYTHONPATH to include libs
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "services.api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]

