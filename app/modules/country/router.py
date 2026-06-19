from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from .models import CountryModel
from .schemas import CountryCreate, CountryResponse

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.post("/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
def create_country(country_in: CountryCreate, db: Session = Depends(get_db)):
    """Record a new country in database."""
    # Validación si ya existe el pais.
    country_exist = db.query(CountryModel).filter(
        CountryModel.country_code == country_in.country_code
    )
    if country_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The country with code '{country_in.country_code}' already exist.",
        )

    # De modelo Pydantic a modelo SqlAlchemy
    country_new = CountryModel(
        country_name=country_in.country_name,
        country_code=country_in.country_code,
    )
    db.add(country_new)
    db.commit()
    db.refresh(country_new)

    return country_new
