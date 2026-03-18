# Pluralia

**Pluralia** is a Spanish news aggregator that classifies articles by political bias, detects sensationalism using LLM analysis, and groups related stories from different sources.

Live: **[pluralia.info](https://pluralia.info)**

---

## Features

- **News aggregation** — Collects articles from 10+ major Spanish outlets via RSS
- **Bias classification** — Sources tagged as left / center / right
- **Sensationalism detection** — Each article scored 0–1 by GPT-4o mini (see [Algorithm](#sensationalism-algorithm))
- **Semantic grouping** — Similar stories across sources clustered using OpenAI embeddings
- **Web frontend** — React SPA with color-coded badges, source filter, cluster view, and algorithm explanation
- **REST API** — FastAPI with `/news` and `/groups` endpoints
- **Automated ingest** — GitHub Actions cron runs twice daily (08:00 and 18:00 UTC)

---

## Architecture

Monorepo following **Domain-Driven Design** and **Clean Architecture**:

```
pluralia/
├── libs/domain/               # Shared domain (entities, value objects, repositories)
├── services/api/              # FastAPI REST API
├── services/ingest/           # RSS ingestion + LLM analysis
├── services/web/              # React + Vite + Tailwind frontend
├── tests/                     # Integration and unit tests
├── docker-compose.yml
├── Makefile
└── fly.toml                   # Fly.io deploy config
```

### Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| API | Python 3.11, FastAPI, Uvicorn |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| Database | PostgreSQL (Neon in production) |
| Migrations | Alembic |
| LLM | OpenAI GPT-4o mini |
| Embeddings | OpenAI text-embedding-ada-002 |
| Containerization | Docker, nginx |

### Production infrastructure

| Service | Platform |
|---|---|
| API | Fly.io (cdg region) |
| Database | Neon (serverless Postgres) |
| Frontend | Vercel |
| Ingest | GitHub Actions cron |

---

## Local development

### Prerequisites

- Docker + Docker Compose
- `OPENAI_API_KEY` (for sensationalism analysis and embeddings)

### Quickstart

```bash
git clone https://github.com/jorgeas80/pluralia.git
cd pluralia

# Start API + DB + Web
make up

# Run database migrations
make migrate

# Run news ingestion (requires OPENAI_API_KEY)
OPENAI_API_KEY=sk-... make ingest
```

- API: http://localhost:8000
- Web: http://localhost:3000
- API docs: http://localhost:8000/docs

### Environment variables

Copy `.env.example` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | local Docker postgres |
| `OPENAI_API_KEY` | OpenAI API key (required for ingest) | — |
| `CORS_ORIGINS` | Comma-separated allowed origins | `*` |
| `VITE_API_URL` | API URL for the web frontend | `http://localhost:8000` |

### Makefile reference

```bash
make up               # Start all services (API + DB + Web)
make down             # Stop all services
make build            # Rebuild Docker images
make migrate          # Run Alembic migrations (requires running API container)
make migrate-remote   # Run migrations against external DB: make migrate-remote DATABASE_URL=...
make ingest           # Run news ingestion
make logs             # Tail all service logs
make logs-api         # Tail API logs
make logs-web         # Tail web logs
make web-build        # Rebuild web image
make test             # Run all tests
make test-unit        # Run unit tests only
make test-integration # Run integration tests only
make test-coverage    # Run tests with HTML coverage report
make shell-api        # Open shell in API container
make shell-db         # Open PostgreSQL shell
make clean-db         # Drop and recreate database (WARNING: deletes all data)
```

---

## API endpoints

### `GET /health`

```json
{ "status": "ok" }
```

### `GET /news?limit=20`

Returns recent articles from all sources.

```json
{
  "news": [
    {
      "id": "uuid",
      "title": "Titular de la noticia",
      "link": "https://...",
      "description": "Descripción breve",
      "published": "2024-01-01T12:00:00",
      "source": "El País",
      "bias": "left",
      "sensationalism_score": 0.42,
      "sensationalism_explanation": "Contiene 2 adjetivos valorativos..."
    }
  ]
}
```

### `GET /groups?limit=50&min_articles=2`

Returns news groups (stories covered by multiple sources), sorted by coverage breadth.

```json
{
  "groups": [
    {
      "id": "uuid",
      "created_at": "2024-01-01T12:00:00",
      "articles": [ /* same structure as /news items */ ]
    }
  ]
}
```

---

## Sensationalism algorithm

Each article is analyzed by **GPT-4o mini** (temperature 0) using its title and RSS description. The model applies a linguistic formula:

### How it works

1. **Assertion Units (H)** — count verifiable facts, data points, and direct quotes in the text.
2. **Subjective adjectives (A)** — count evaluative or emotional adjectives (e.g. "brutal", "vergonzoso", "preocupante"). Neutral/technical adjectives (e.g. "pública", "anual") are excluded.
3. **Formula:**

```
IS = A / (A + H)        (if A = 0 and H = 0, IS = 0)
```

The result is naturally bounded between 0 and 1. IS > 0.5 indicates sensationalist predominance.

### Color scale

| Score | Level | Color |
|---|---|---|
| null | No data | Grey |
| 0.00 – 0.33 | Low | Green |
| 0.34 – 0.66 | Medium | Amber |
| 0.67 – 1.00 | High | Red |

### Limitations

- Analysis is based only on title + RSS description, not the full article.
- The model may make errors on very short or ambiguous titles.
- The index measures linguistic sensationalism, not factual accuracy or political bias.
- Sources with a more direct writing style will systematically score lower.

---

## Data flow

```
GitHub Actions (cron 08:00 / 18:00 UTC)
    │
    ▼
services/ingest
    ├── Parse RSS feeds → extract articles
    ├── Generate OpenAI embeddings → semantic grouping into NewsGroups
    ├── Analyze sensationalism via GPT-4o mini → score + explanation
    └── Persist to PostgreSQL (Neon)
    │
    ▼
services/api  (Fly.io)
    ├── GET /news   → returns articles with bias + sensationalism
    └── GET /groups → returns clusters (embedding column excluded)
    │
    ▼
services/web  (Vercel)
    ├── Noticias tab    → article list with color-coded badges
    ├── Clusters tab    → grouped stories by topic
    ├── Fuentes tab     → per-source stats (avg score, bias, count)
    └── Cómo funciona   → algorithm explanation
```

---

## Domain architecture

The project follows **Domain-Driven Design**:

- **Entities**: `Source`, `Article`, `NewsGroup` — objects with unique identity
- **Value Objects**: `Bias`, `TopicHash` — immutable, no identity
- **Repositories**: interfaces in `libs/domain`, implementations in each service's infrastructure layer
- **Use Cases**: application logic orchestrating domain operations (`GetNews`, `GetGroups`, `IngestNews`)

---

## Contributing

1. Fork the project
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit your changes
4. Push and open a Pull Request against `main`

---

## License

MIT — see `LICENSE`.

---

*Developed to promote informational pluralism in Spanish media.*
