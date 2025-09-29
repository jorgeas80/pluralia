FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala deps
COPY backend/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

# Copia la app
COPY backend /app/backend

EXPOSE 8000
# Usa el $PORT de Railway si existe; si no, 8000
CMD ["sh","-c","python -m uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
