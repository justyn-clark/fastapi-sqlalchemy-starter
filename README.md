# FastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL

A clean, minimal FastAPI starter template with:

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **Alembic** - Database migrations
- **Pydantic** - Data validation and serialization
- **JWT Authentication** - Built-in auth system

## Quick start

```bash
# 1) Create virtualenv & install deps
python -m venv .venv && source .venv/bin/activate  # Linux/Mac
# or python -m venv .venv && .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2) Create database
createdb fastapi_starter  # or: psql -c 'CREATE DATABASE fastapi_starter;'

# 3) Run migrations
alembic upgrade head

# 4) Start the API
uvicorn app.main:app --reload
```

### Notes

- App uses **async engine** via `postgresql+asyncpg`
- Alembic uses **sync driver** (`psycopg`) for migrations
- Default entity: `User` with endpoints:
  - `POST /auth/register` - Register new user
  - `POST /auth/login` - Login and get JWT token
  - `POST /users` - Create user (admin)
  - `GET /users` - List all users
  - `GET /users/{id}` - Get user by ID

## Environment Setup

Create a `.env` file:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_starter
APP_HOST=127.0.0.1
APP_PORT=8000
```

## Migration commands

```bash
# Generate a new migration (after editing models)
alembic revision --autogenerate -m "describe changes"

# Apply migrations
alembic upgrade head

# Downgrade one
alembic downgrade -1
```

## Testing the API

```bash
# Register a new user
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"password123"}'

# Login to get JWT token
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# List users (requires authentication)
curl -X GET http://127.0.0.1:8000/users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Docker Development

```bash
# Start database and API
docker compose up -d --build

# View logs
docker compose logs -f api

# Stop everything
docker compose down -v
```

- API: <http://localhost:8000>
- Database: localhost:5434 (postgres/postgres)

## Development Commands

```bash
# Format code
make fmt

# Lint code
make lint

# Type checking
make type

# Run tests
make test

# OpenAPI spec
make openapi
```

## Authentication

The API includes JWT-based authentication:

1. **Register**: `POST /auth/register` with email, password, and optional full_name
2. **Login**: `POST /auth/login` with email and password to get JWT token
3. **Protected routes**: Include `Authorization: Bearer <token>` header

All user management endpoints require authentication.
