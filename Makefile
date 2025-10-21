SHELL := /bin/bash
.ONESHELL:

PY := python
PIP := pip

# Load env if present
ifneq (,$(wildcard .env))
  include .env
  export
endif

.PHONY: setup run fmt lint type test revision migrate up down logs alembic

setup:
	$(PY) -m venv .venv && source .venv/bin/activate && $(PIP) install -r requirements.txt
	pre-commit install

run:
	uvicorn app.main:app --reload --host $${APP_HOST:-127.0.0.1} --port $${APP_PORT:-8000}

fmt:
	ruff format .

lint:
	ruff .

type:
	mypy app

test:
	pytest -q

revision:
	alembic revision --autogenerate -m "$${m:-changes}"

migrate:
	alembic upgrade head

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200


openapi:
	$(PY) scripts/export_openapi.py
