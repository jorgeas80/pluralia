FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala deps
COPY api/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

# Copia la app
COPY api /app/api

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

