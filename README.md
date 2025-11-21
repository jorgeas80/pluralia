# Pluralia 📰

**Pluralia** is a news aggregation API that collects information from multiple Spanish media sources, classifying them by political bias and grouping them by topics to provide a plural view of current events.

## 🎯 Features

- **News aggregation**: Collects news from 10+ major Spanish media outlets
- **Bias classification**: Categorizes sources according to their political orientation (left, center, right)
- **Thematic grouping**: Groups similar news using title hashing
- **REST API**: Endpoints to query news and metrics
- **PostgreSQL database**: Persistent storage of articles and sources
- **Docker**: Complete containerization for development and production
- **Monorepo architecture**: Separated services following Domain-Driven Design

## 🏗️ Architecture

The project is structured as a **monorepo** following **Domain-Driven Design (DDD)** and **Clean Architecture** principles:

- **libs/domain**: Shared domain code (entities, value objects, repositories)
- **services/api**: REST API service (FastAPI)
- **services/ingest**: News ingestion service from RSS feeds
- **services/web**: Web frontend (pending implementation)

### Technologies

- **FastAPI**: Modern and fast web framework for Python
- **SQLModel**: ORM that combines SQLAlchemy with Pydantic
- **PostgreSQL**: Relational database for persistence
- **feedparser**: Library for parsing RSS/Atom feeds
- **Docker Compose**: Service orchestration

## 📁 Project Structure

```
pluralia/
├── libs/
│   └── domain/                    # Shared domain code
│       ├── entities/              # Domain entities (Source, Article, NewsGroup)
│       ├── value_objects/         # Value Objects (Bias, TopicHash)
│       ├── repositories/          # Repository interfaces
│       └── errors/                # Domain exceptions
├── services/
│   ├── api/                       # REST API service
│   │   ├── src/
│   │   │   ├── domain/            # API-specific domain logic
│   │   │   ├── application/       # Use cases
│   │   │   └── infrastructure/    # Technical implementations
│   │   │       ├── api/           # FastAPI controllers/routes
│   │   │       ├── repositories/  # Repository implementations
│   │   │       └── database/      # SQLModel models and DB configuration
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── ingest/                    # Ingestion service
│   │   ├── src/
│   │   │   ├── domain/
│   │   │   ├── application/       # Ingestion use cases
│   │   │   └── infrastructure/
│   │   │       ├── repositories/
│   │   │       ├── services/      # Technical services (RSS parser)
│   │   │       └── database/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── web/                       # Frontend (pending)
│       └── src/
├── docker-compose.yml             # Orchestration of all services
├── setup.py                       # Configuration for libs imports
└── README.md                      # This file
```

## 🚀 Installation and Local Development

### Prerequisites

- **Docker** and **Docker Compose**
- **Python 3.11+** (for local development without Docker)
- **PostgreSQL** (if running without Docker)

### Option 1: Development with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pluralia
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Verify everything works**:
   ```bash
   # Verify the API responds
   curl http://localhost:8000/health
   
   # Verify the database is available
   docker-compose logs db
   ```

4. **Run the initial news ingestion**:
   ```bash
   docker-compose run --rm pluralia-ingest python -m services.ingest.src.main
   ```

5. **Access the API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Option 2: Local Development (Without Docker)

1. **Install dependencies**:
   ```bash
   # Install API dependencies
   cd services/api
   pip install -r requirements.txt
   
   # Install ingest dependencies
   cd ../ingest
   pip install -r requirements.txt
   ```

2. **Configure PostgreSQL**:
   - Install PostgreSQL locally
   - Create a database named `pluralia`
   - Set environment variables:
     ```bash
     export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pluralia"
     export PYTHONPATH="${PYTHONPATH}:$(pwd)"
     ```

3. **Run the API application**:
   ```bash
   cd services/api
   uvicorn services.api.src.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run the ingestion**:
   ```bash
   cd services/ingest
   python -m services.ingest.src.main
   ```

## 📊 API Endpoints

### `GET /health`
Checks the API status.

**Response**:
```json
{
  "status": "ok"
}
```

### `GET /news`
Gets recent news from multiple sources.

**Parameters**:
- `limit` (optional): Number of news items per source (default: 20)

**Response**:
```json
{
  "news": [
    {
      "id": "uuid",
      "title": "News title",
      "link": "https://example.com/news",
      "description": "News description",
      "published": "2024-01-01T12:00:00",
      "source": "El País",
      "bias": "left"
    }
  ]
}
```

## 🔧 Useful Commands

### Docker Compose

```bash
# Start services (only API and DB, ingest does NOT start automatically)
docker-compose up -d

# View logs from all services
docker-compose logs -f

# View logs from a specific service
docker-compose logs -f pluralia-api

# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache

# Run ingestion manually (runs, ingests news, and exits)
docker-compose run --rm pluralia-ingest python -m services.ingest.src.main

# Or using the profile (if you want to start it as a service)
docker-compose --profile ingest up -d pluralia-ingest

# Access the database
docker-compose exec db psql -U postgres -d pluralia

# Run tests
docker-compose --profile test run --rm pluralia-test pytest

# Run tests with coverage
docker-compose --profile test run --rm pluralia-test pytest --cov=libs --cov=services --cov-report=html
```

### Schedule automatic ingestion

The `ingest` service is configured with a `profile`, so it **does NOT start automatically** with `docker-compose up -d`. It only runs when explicitly invoked.

**Option 1: Cron job (Linux/Mac)**

Add this line to your crontab (`crontab -e`):

```bash
# Run ingestion every hour
0 * * * * cd /full/path/to/pluralia && docker-compose run --rm pluralia-ingest python -m services.ingest.src.main >> /var/log/pluralia-ingest.log 2>&1

# Run ingestion every 30 minutes
*/30 * * * * cd /full/path/to/pluralia && docker-compose run --rm pluralia-ingest python -m services.ingest.src.main >> /var/log/pluralia-ingest.log 2>&1
```

**Option 2: Task Scheduler (Windows)**

Create a scheduled task that runs:

```powershell
cd C:\path\to\pluralia
docker-compose run --rm pluralia-ingest python -m services.ingest.src.main
```

**Option 3: Systemd timer (Linux)**

Create `/etc/systemd/system/pluralia-ingest.service`:

```ini
[Unit]
Description=Pluralia News Ingest
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=/path/to/pluralia
ExecStart=/usr/bin/docker-compose run --rm pluralia-ingest python -m services.ingest.src.main
```

And `/etc/systemd/system/pluralia-ingest.timer`:

```ini
[Unit]
Description=Run Pluralia Ingest hourly

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

Then enable the timer:
```bash
sudo systemctl enable pluralia-ingest.timer
sudo systemctl start pluralia-ingest.timer
```

### Development

```bash
# Run news ingestion
python -m services.ingest.src.main

# Run tests (when implemented)
pytest

# Format code
black services/ libs/

# Linting
flake8 services/ libs/
```

## 🗄️ Database

### Main Models

- **Source**: News sources with their political bias
- **Article**: Individual articles
- **NewsGroup**: Groups of related news by topic

### Migrations

The database is automatically initialized when running the application for the first time.

## 🔄 Data Flow

1. **Ingestion**: The `ingest` service parses RSS feeds from multiple sources
2. **Classification**: Each source has an assigned political bias (left, center, right)
3. **Grouping**: Articles are grouped by title similarity using SHA256 hashing
4. **Storage**: Data is saved to PostgreSQL
5. **API**: The `api` service exposes data for consumption through REST endpoints

## 🏛️ Domain Architecture

The project follows **Domain-Driven Design (DDD)**:

- **Entities**: `Source`, `Article`, `NewsGroup` - Objects with unique identity
- **Value Objects**: `Bias`, `TopicHash` - Immutable objects without identity
- **Repositories**: Interfaces in the domain, implementations in infrastructure
- **Use Cases**: Application logic orchestrating domain operations

## 🛠️ Technologies Used

- **Python 3.11**
- **FastAPI** - Web framework
- **SQLModel** - ORM and validation
- **PostgreSQL** - Database
- **feedparser** - RSS feed parsing
- **Docker** - Containerization
- **Uvicorn** - ASGI server

## 📝 Development Notes

- The project uses **SQLModel** which combines SQLAlchemy with Pydantic
- RSS feeds are updated by running the ingestion service
- News grouping uses SHA256 hashing of normalized titles
- Domain code is in `libs/domain` and is shared between services
- Each service has its own repository implementations in the infrastructure layer

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is under the MIT License. See the `LICENSE` file for more details.

---

**Developed with ❤️ to promote informational pluralism**
