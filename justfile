set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

default:
    @just --list

setup:
    python -m venv .venv
    source .venv/bin/activate && pip install -r requirements.txt
    pre-commit install

run:
    uvicorn app.main:app --reload --host "${APP_HOST:-127.0.0.1}" --port "${APP_PORT:-8000}"

fmt:
    ruff format .

lint:
    ruff check .

type:
    mypy app

test:
    pytest -q

revision message="changes":
    alembic revision --autogenerate -m "{{message}}"

migrate:
    alembic upgrade head

up:
    docker compose up -d --build

down:
    docker compose down -v

logs:
    docker compose logs -f --tail=200

openapi:
    python scripts/export_openapi.py
