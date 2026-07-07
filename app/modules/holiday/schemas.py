from datetime import date, datetime

from pydantic import BaseModel, Field


class HolidayDB(BaseModel):
    holiday_date: date = Field(..., description="Día festivo")
    holiday_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nombre del día festivo",
    )
    holiday_description: str | None = Field(
        default=None,
        max_length=512,
        description="Descripción del día festivo.",
    )
    holiday_type: str | None = Field(
        default=None,
        max_length=50,
        description="Tipo de día festivo.",
    )
    holiday_is_substitutable: bool | None = Field(
        default=None,
        description="Indica si el día festivo es sustituible.",
    )
    holiday_is_mandatory: bool | None = Field(
        default=None,
        description="Indica si el día festivo es obligatorio.",
    )
    holiday_law_reference: str | None = Field(
        default=None,
        max_length=255,
        description="Referencia legal del día festivo.",
    )
    id_country: int = Field(..., gt=0, description="ID del país.")


class HolidayCreate(HolidayDB):
    pass


class HolidayResponse(HolidayDB):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
