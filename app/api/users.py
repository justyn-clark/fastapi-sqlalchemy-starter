from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_db
from ..schemas.auth import RegisterRequest
from ..schemas.user import UpdateUserDto, User
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    payload: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Create a new user"""
    service = UserService(db)
    return await service.create(payload)


@router.get("", response_model=list[User])
async def list_users_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[User]:
    """Get all users"""
    service = UserService(db)
    return await service.find_all()


@router.get("/{user_id}", response_model=User)
async def get_user_endpoint(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get user by ID"""
    service = UserService(db)
    user = await service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/{user_id}/details", response_model=User)
async def get_user_details_endpoint(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get user with details"""
    service = UserService(db)
    user = await service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/email/{email}", response_model=User)
async def get_user_by_email_endpoint(
    email: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get user by email"""
    service = UserService(db)
    user = await service.find_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/search", response_model=list[User])
async def search_users_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, description="Maximum number of results"),
) -> list[User]:
    """Search users by name or email"""
    # For now, return all users since search functionality is not implemented in the simple service
    service = UserService(db)
    return await service.find_all()


@router.put("/{user_id}", response_model=User)
async def update_user_endpoint(
    user_id: int,
    payload: UpdateUserDto,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Update user"""
    service = UserService(db)
    return await service.update(user_id, payload)


@router.delete("/{user_id}")
async def delete_user_endpoint(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Delete user"""
    service = UserService(db)
    await service.remove(user_id)
    return {"message": "User deleted successfully"}


# Additional endpoints removed for simplicity - this is a clean starter template
# Users can add these back as needed for their specific use case
