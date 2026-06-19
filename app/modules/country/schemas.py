from datetime import datetime

from pydantic import BaseModel, Field


# Clase con los campos que se van a crear. Esto es la base.
class CountryDB(BaseModel):
    country_name: str = Field(
        ..., min_length=2, max_length=50, description="Nombre de país"
    )
    country_code: str = Field(
        ..., min_length=2, max_length=3, description="Código ISO (ej. PE, USA)"
    )


# Esta clase hereda de CountryDB sirve para agregar algún campo adicional
class CountryCreate(CountryDB):
    pass


class CountryResponse(CountryDB):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
