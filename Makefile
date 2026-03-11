.PHONY: help up down build logs test clean-db ingest

help: ## Show this help message
	@echo "Available commands:"
	@echo "  up              Start all services (API + DB)"
	@echo "  down            Stop all services"
	@echo "  build           Rebuild all Docker images"
	@echo "  logs            Show logs from all services"
	@echo "  logs-api        Show logs from API service"
	@echo "  logs-db         Show logs from database"
	@echo "  test            Run all tests"
	@echo "  test-unit       Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-coverage   Run tests with coverage report"
	@echo "  clean-db        Drop and recreate database (WARNING: deletes all data)"
	@echo "  recreate-db     Recreate database tables (drops existing tables)"
	@echo "  ingest          Run news ingestion"
	@echo "  shell-api        Open shell in API container"
	@echo "  shell-db         Open PostgreSQL shell"
	@echo "  restart-api      Restart API service"
	@echo "  migrate          Run database migrations"
	@echo "  migrate-create   Create a new migration (usage: make migrate-create MESSAGE=\"description\")"

up: ## Start all services (API + DB)
	docker-compose up -d

down: ## Stop all services
	docker-compose down

build: ## Rebuild all Docker images
	docker-compose build --no-cache

logs: ## Show logs from all services
	docker-compose logs -f

logs-api: ## Show logs from API service
	docker-compose logs -f pluralia-api

logs-db: ## Show logs from database
	docker-compose logs -f db

test: ## Run all tests
	docker-compose --profile test run --rm pluralia-test pytest

test-unit: ## Run unit tests only
	docker-compose --profile test run --rm pluralia-test pytest tests/unit

test-integration: ## Run integration tests only
	docker-compose --profile test run --rm pluralia-test pytest tests/integration

test-coverage: ## Run tests with coverage report
	docker-compose --profile test run --rm pluralia-test pytest --cov=libs --cov=services --cov-report=html

clean-db: ## Drop and recreate database (WARNING: deletes all data)
	docker-compose down -v
	-docker volume rm pluralia_db_data
	docker-compose up -d db
	@echo "✅ Database cleaned. Tables will be recreated on next service start."
	@echo "💡 To recreate tables, start services with: make recreate-db"

recreate-db: ## Recreate database tables (drops existing tables)
	@echo "Setting DROP_DB=true and starting services..."
	@echo "Note: If this fails on Windows, run manually:"
	@echo "  set DROP_DB=true && docker-compose up -d"
	@echo "Or: DROP_DB=true docker-compose up -d (Git Bash/WSL)"
ifeq ($(OS),Windows_NT)
	cmd //c "set DROP_DB=true && docker-compose up -d"
else
	DROP_DB=true docker-compose up -d
endif
	@echo "✅ Database tables will be recreated on service start"

ingest: ## Run news ingestion
	docker-compose run --rm pluralia-ingest python -m services.ingest.src.main

shell-api: ## Open shell in API container
	docker-compose exec pluralia-api /bin/bash

shell-db: ## Open PostgreSQL shell
	docker-compose exec db psql -U postgres -d pluralia

restart-api: ## Restart API service
	docker-compose restart pluralia-api

migrate: ## Run database migrations
	docker-compose exec pluralia-api sh -c "cd services/api && alembic upgrade head"

migrate-create: ## Create a new migration (usage: make migrate-create MESSAGE="description")
	docker-compose exec pluralia-api sh -c "cd services/api && alembic revision --autogenerate -m '$(MESSAGE)'"

