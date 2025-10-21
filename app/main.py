from fastapi import FastAPI

from .api.auth import router as auth_router
from .api.users import router as users_router
from .deps import lifespan

app: FastAPI = FastAPI(title="FastAPI + SQLAlchemy Async + Alembic", lifespan=lifespan)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
