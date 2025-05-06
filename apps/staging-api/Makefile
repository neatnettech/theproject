# Makefile for FastAPI + Poetry + Dependency Injector project

ENV ?= development
PYTHON := poetry run python
UVICORN := poetry run uvicorn
PYTEST := poetry run pytest

APP_MODULE := app:app
PORT ?= 8000
HOST ?= 0.0.0.0
PYTHONPATH := .

.PHONY: help install run dev test lint format clean seed debug drop-db

help:
	@echo "Available targets:"
	@echo "  install       Install dependencies"
	@echo "  run           Run app using Gunicorn/Uvicorn"
	@echo "  dev           Run app in development mode (Uvicorn with reload)"
	@echo "  test          Run tests using pytest-bdd"
	@echo "  lint          Lint code using Ruff"
	@echo "  format        Format code using Black"
	@echo "  clean         Clean __pycache__ and .pytest_cache"

install:
	PYTHONPATH=$(PYTHONPATH) poetry install

docker-dev:
	cp .env.docker.dev .env || true
	docker compose --project-name the-project --env-file .env.docker.dev up --build
run:
	PYTHONPATH=$(PYTHONPATH) $(UVICORN) $(APP_MODULE) --host $(HOST) --port $(PORT)

dev:
	PYTHONPATH=$(PYTHONPATH) $(UVICORN) $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

debug:
	DEBUGPY=1 PYTHONPATH=$(PYTHONPATH) poetry run uvicorn app:app --host $(HOST) --port $(PORT) --reload

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/

lint:
	PYTHONPATH=$(PYTHONPATH) poetry run ruff app tests

format:
	PYTHONPATH=$(PYTHONPATH) poetry run black app tests

seed:
	PYTHONPATH=$(PYTHONPATH) poetry run python scripts/seed_nodes.py

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cach


seed-db:
	PYTHONPATH=$(PYTHONPATH) poetry run python -c "from app.database import seed_db; seed_db()"


# Drop all tables from PostgreSQL (DANGER: destructive!)
drop-db:
	@echo "⚠️  Dropping all tables inside the Postgres container..."
	docker exec -e PGPASSWORD=postgres the-project-db \
	psql -U postgres -d the_project_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@echo "✅ All tables dropped and schema recreated."