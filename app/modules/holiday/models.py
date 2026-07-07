from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import base


class HolidayModel(base):
    __tablename__ = "holiday"
    __table_args__ = {"schema": "holiday"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    holiday_date = Column(Date, nullable=False)
    holiday_name = Column(String(255), nullable=False)
    holiday_description = Column(String(512), nullable=True)
    holiday_type = Column(String(50), nullable=True)
    holiday_is_substitutable = Column(Boolean, nullable=True)
    holiday_is_mandatory = Column(Boolean, nullable=True)
    holiday_law_reference = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    id_country = Column(
        Integer,
        ForeignKey("holiday.country.id"),
        nullable=False,
    )

    # Relación: Permite acceder a 'holiday.country' para saber a qué país pertenece la festividad
    country = relationship("CountryModel", back_populates="holiday")
