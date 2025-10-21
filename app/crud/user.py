from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.auth import hash_password
from ..models.user import User
from ..schemas.auth import RegisterRequest


async def create_user(db: AsyncSession, data: RegisterRequest) -> User:
    user = User(
        email=data.email, full_name=data.full_name, password_hash=hash_password(data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def list_users(db: AsyncSession) -> list[User]:
    res = await db.execute(select(User).order_by(User.id))
    return list(res.scalars())
