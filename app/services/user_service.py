"""
Simple user service for basic CRUD operations
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.auth import hash_password
from ..models.user import User as UserModel
from ..schemas.auth import RegisterRequest
from ..schemas.user import UpdateUserDto, User


class UserService:
    """Simple user service class with basic CRUD operations"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _map_to_user(self, db_user: UserModel) -> User:
        """Map database user to response model"""
        return User(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
        )

    async def create(self, register_request: RegisterRequest) -> User:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = await self.db.execute(
                select(UserModel).where(UserModel.email == register_request.email)
            )
            if existing_user.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists",
                )

            # Create new user
            new_user = UserModel(
                email=register_request.email,
                full_name=register_request.full_name,
                password_hash=hash_password(register_request.password),
            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)

            return self._map_to_user(new_user)

        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {e!s}",
            ) from e

    async def find_all(self) -> list[User]:
        """Find all users"""
        try:
            result = await self.db.execute(select(UserModel).order_by(UserModel.id))
            users = result.scalars().all()
            return [self._map_to_user(user) for user in users]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch users: {e!s}",
            ) from e

    async def find_by_id(self, user_id: int) -> User | None:
        """Find user by ID"""
        try:
            result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
            user = result.scalar_one_or_none()
            return self._map_to_user(user) if user else None

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user: {e!s}",
            ) from e

    async def find_by_email(self, email: str) -> User | None:
        """Find user by email"""
        try:
            result = await self.db.execute(select(UserModel).where(UserModel.email == email))
            user = result.scalar_one_or_none()
            return self._map_to_user(user) if user else None

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user: {e!s}",
            ) from e

    async def update(self, user_id: int, update_user_dto: UpdateUserDto) -> User:
        """Update user"""
        try:
            result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            # Update fields
            if update_user_dto.email is not None:
                user.email = update_user_dto.email
            if update_user_dto.full_name is not None:
                user.full_name = update_user_dto.full_name

            await self.db.commit()
            await self.db.refresh(user)

            return self._map_to_user(user)

        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user: {e!s}",
            ) from e

    async def remove(self, user_id: int) -> None:
        """Delete user"""
        try:
            result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            await self.db.delete(user)
            await self.db.commit()

        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete user: {e!s}",
            ) from e
