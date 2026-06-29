import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, String
from sqlalchemy.sql import func

from app.core.database import base


class UserModel(base):
    __tablename__ = "user"
    __table_args__ = {"schema": "holiday"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
