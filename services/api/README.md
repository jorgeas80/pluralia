# Pluralia API Service

REST API service for the Pluralia news aggregation platform. This service exposes endpoints to query news articles from multiple Spanish media sources, classified by political bias and grouped by topics.

## Overview

The API service is built with **FastAPI** and follows **Domain-Driven Design (DDD)** principles. It provides a clean REST interface to access aggregated news data stored in PostgreSQL.

## Architecture

The service is structured in three layers:

- **Domain Layer** (`libs/domain`): Shared domain entities, value objects, and repository interfaces
- **Application Layer** (`src/application`): Use cases that orchestrate domain operations
- **Infrastructure Layer** (`src/infrastructure`): Technical implementations
  - `api/`: FastAPI routes and controllers
  - `database/`: SQLModel models and database configuration
  - `repositories/`: Repository implementations for data persistence

## API Endpoints

### `GET /health`

Health check endpoint to verify the API is running.

**Response**:
```json
{
  "status": "ok"
}
```

### `GET /news`

Retrieves recent news articles from all sources.

**Query Parameters**:
- `limit` (optional, default: 20): Maximum number of articles per source

**Response**:
```json
{
  "news": [
    {
      "id": "uuid",
      "title": "Article title",
      "link": "https://example.com/article",
      "description": "Article description",
      "published": "2024-01-01T12:00:00",
      "source": "El País",
      "bias": "left"
    }
  ]
}
```

## Development

### Prerequisites

- Python 3.11+
- PostgreSQL (or use Docker Compose)
- Docker and Docker Compose (optional, recommended)

### Local Development

1. **Install dependencies**:
   ```bash
   cd services/api
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pluralia"
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/../.."
   ```

3. **Run the API**:
   ```bash
   uvicorn services.api.src.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Development

The service is containerized and can be run with Docker Compose:

```bash
# Start all services (API + DB)
docker-compose up -d

# View API logs
docker-compose logs -f pluralia-api

# Stop services
docker-compose down
```

## Project Structure

```
services/api/
├── src/
│   ├── application/          # Use cases
│   │   └── get_news.py      # GetNews use case
│   ├── infrastructure/       # Technical implementations
│   │   ├── api/             # FastAPI routes
│   │   │   └── routes.py    # API endpoint definitions
│   │   ├── database/        # Database configuration
│   │   │   ├── db.py        # Database connection and session management
│   │   │   └── models.py    # SQLModel database models
│   │   └── repositories/    # Repository implementations
│   │       ├── sqlmodel_article_repository.py
│   │       └── sqlmodel_source_repository.py
│   └── main.py              # FastAPI application entry point
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLModel**: ORM combining SQLAlchemy and Pydantic
- **Uvicorn**: ASGI server for running FastAPI
- **PostgreSQL**: Database driver (via SQLModel)

## Database

The service uses PostgreSQL for data persistence. The database is automatically initialized when the service starts via `init_db()`, which:

1. Drops existing tables (for development)
2. Creates tables with correct schema (UUID-based IDs)

### Models

- **SourceModel**: News sources with political bias
- **ArticleModel**: Individual news articles
- **NewsGroupModel**: Groups of related articles by topic

## Testing

Tests should be placed in the `tests/` directory at the project root, following the structure:

```
tests/
├── unit/
│   └── application/         # Unit tests for use cases
└── integration/
    └── api/                 # Integration tests for API endpoints
```

## Contributing

When adding new endpoints:

1. Define the use case in `src/application/`
2. Add the route in `src/infrastructure/api/routes.py`
3. Update this README with endpoint documentation
4. Add tests in `tests/integration/api/`

## Related Services

- **ingest**: Service responsible for ingesting news from RSS feeds
- **web**: Frontend service (pending implementation)

