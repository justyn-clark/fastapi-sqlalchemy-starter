from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.auth import create_access_token, verify_password
from ..deps import get_db
from ..models.user import User as UserModel
from ..schemas.auth import LoginRequest, RegisterRequest, Token
from ..schemas.user import User
from ..services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]) -> User:
    service = UserService(db)
    return await service.create(payload)


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]) -> Token:
    res = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "email": user.email})
    return {"access_token": token, "token_type": "bearer"}
