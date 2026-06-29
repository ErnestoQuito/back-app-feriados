from datetime import datetime

from pydantic import BaseModel, Field


class UserDB(BaseModel):
    email: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="correo electrónico.",
    )
    is_active: bool = Field(..., description="¿El usuario esta activo?")
    role: str = Field(..., min_length=3, max_length=50, description="Rol del usuario.")


class UserCreate(UserDB):
    password_hash: str


class UserResponse(UserDB):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
