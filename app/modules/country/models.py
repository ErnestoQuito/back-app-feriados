from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import base


class CountryModel(base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(
        String(50),
        nullable=False,
    )
    country_code = Column(String(3), nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
