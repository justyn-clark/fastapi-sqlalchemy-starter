from pydantic import BaseModel, EmailStr


class UpdateUserDto(BaseModel):
    email: str | None = None
    full_name: str | None = None


class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
