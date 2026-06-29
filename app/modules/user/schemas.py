import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None


class UserDB(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=2,
        max_length=255,
        description="correo electrónico.",
    )
    is_active: bool = Field(..., description="¿El usuario esta activo?")
    role: str = Field(..., min_length=3, max_length=50, description="Rol del usuario.")


class UserCreate(UserDB):
    pass


class UserResponse(UserDB):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
