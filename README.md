# FastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1C1C1C?style=for-the-badge&logo=sqlalchemy)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

A clean, minimal FastAPI starter template with:

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **Alembic** - Database migrations
- **Pydantic** - Data validation and serialization
- **JWT Authentication** - Built-in auth system

## Features

<div align="center">

![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-blue?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge)
![Type Check](https://img.shields.io/badge/Type%20Check-MyPy-blue?style=for-the-badge)
![Linting](https://img.shields.io/badge/Linting-Ruff-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

- ✅ **Production Ready** - Complete CI/CD pipeline with GitHub Actions
- ✅ **Type Safe** - Full mypy type checking and Pydantic validation
- ✅ **Async First** - Modern async/await patterns throughout
- ✅ **Docker Support** - Ready-to-use Docker configuration
- ✅ **Database Migrations** - Alembic integration for schema management
- ✅ **JWT Authentication** - Secure token-based auth system
- ✅ **OpenAPI Documentation** - Auto-generated Swagger UI
- ✅ **Testing Setup** - Comprehensive test configuration

## API Documentation

<div align="center">

![Swagger UI](https://img.shields.io/badge/API%20Docs-Swagger%20UI-green?style=for-the-badge)

*Interactive API documentation available at `/docs`*

</div>

### Screenshot

<div align="center">

<img src="docs/swagger-screenshot.png" alt="API Documentation" width="600" style="max-width: 100%; height: auto;">

*Interactive Swagger UI showing all available endpoints*

</div>

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you found this starter template helpful, please give it a ⭐ star!

---

<div align="center">

**Made with ❤️ for the FastAPI community**

[![GitHub stars](https://img.shields.io/github/stars/justyn-clark/fastapi-sqlalchemy-starter?style=social)](https://github.com/justyn-clark/fastapi-sqlalchemy-starter)
[![GitHub forks](https://img.shields.io/github/forks/justyn-clark/fastapi-sqlalchemy-starter?style=social)](https://github.com/justyn-clark/fastapi-sqlalchemy-starter)

</div>
