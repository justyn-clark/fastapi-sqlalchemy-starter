# FastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL

Minimal starter API built with FastAPI, async SQLAlchemy, Alembic migrations, and PostgreSQL.

## What is in this starter

- FastAPI app with `/docs` and `/openapi.json`
- Async SQLAlchemy setup for runtime database access
- Alembic migrations using a sync PostgreSQL driver
- User model plus auth and user-management routes
- JWT token issuance for login
- Ruff, mypy, pytest, pre-commit, and GitHub Actions CI
- Docker Compose setup for API + PostgreSQL + Adminer (+ Redis container scaffolded but unused by the app)
- `Makefile` and `justfile` task runners

## Current status

This repo is a starter template, not a finished product. A few things are intentionally minimal right now:

- Auth endpoints exist and JWTs are issued, but the `/users` routes are **not currently protected** by an auth dependency.
- `GET /users/search` currently returns all users; real query filtering is not implemented yet.
- The Docker Compose stack includes Redis, but the application code does not use Redis yet.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x (async)
- Alembic
- PostgreSQL 16
- Pydantic Settings
- Ruff
- mypy
- pytest

## Project layout

```text
app/
  api/        # FastAPI route modules
  core/       # config, auth, db setup
  crud/       # data access helpers
  models/     # SQLAlchemy models
  schemas/    # request/response models
  services/   # business logic
alembic/      # migrations
scripts/      # helper scripts such as OpenAPI export
docs/         # generated OpenAPI artifact and README assets
tests/        # test suite
```

## Quick start

### Option A: local Python + local PostgreSQL

```bash
# 1) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt
pre-commit install

# 3) Create local env file
cp .env.example .env

# 4) Create the database
createdb fastapi_starter
# or: psql -c 'CREATE DATABASE fastapi_starter;'

# 5) Run migrations
alembic upgrade head

# 6) Start the API
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Option B: Docker Compose

```bash
docker compose up -d --build
```

Services exposed by the default compose stack:

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- PostgreSQL: `localhost:5434` (`postgres` / `postgres`, database `mydb`)
- Adminer: <http://localhost:8080>
- Redis: `localhost:6379`

Stop and remove volumes:

```bash
docker compose down -v
```

## Environment configuration

Copy `.env.example` to `.env` for local development.

Important settings:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_starter
# Optional: explicit sync URL for Alembic
# DATABASE_URL_SYNC=postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_starter
APP_HOST=127.0.0.1
APP_PORT=8000
# Optional JWT settings
# SECRET_KEY=your-secret-key-here
# ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

Notes:

- The application uses the async PostgreSQL driver (`asyncpg`) at runtime.
- Alembic uses `psycopg` for migrations.
- In Docker Compose, `.env.docker` points the app at the `db` service and uses database `mydb`.

## Available routes

### Utility

- `GET /health`
- `GET /docs`
- `GET /openapi.json`

### Auth

- `POST /auth/register`
- `POST /auth/login`

### Users

- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `GET /users/{user_id}/details`
- `GET /users/email/{email}`
- `GET /users/search?q=...&limit=...`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

## Common development commands

You can use either `make` or `just`.

```bash
# install deps and hooks
make setup
# or
just setup

# run dev server
make run
# or
just run

# format
make fmt
# or
just fmt

# lint
make lint
# or
just lint

# type check
make type
# or
just type

# run tests
make test
# or
just test

# create migration
make revision m="describe changes"
# or
just revision "describe changes"

# apply migrations
make migrate
# or
just migrate

# export OpenAPI spec to docs/openapi.json
make openapi
# or
just openapi
```

## CI

GitHub Actions runs the following on pushes to `main` and on pull requests:

- PostgreSQL service container
- dependency install
- Alembic migrations
- Ruff lint
- mypy type check
- pytest
- OpenAPI export artifact upload

Workflow file: `.github/workflows/ci.yml`

## API docs

Interactive Swagger UI is available at `/docs` when the app is running.

The repo also includes:

- `docs/openapi.json` — exported OpenAPI artifact
- `docs/swagger-screenshot.png` — README asset

## Testing the API

```bash
# Register a user
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"password123"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# List users
curl -X GET http://127.0.0.1:8000/users
```

## Screenshot

<img src="docs/swagger-screenshot.png" alt="Swagger UI screenshot" width="600">

## License

MIT. See [LICENSE](LICENSE).
