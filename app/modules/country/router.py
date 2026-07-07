from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.user.dependencies import get_current_user
from app.modules.user.models import UserModel
from main import limiter

from .models import CountryModel
from .schemas import CountryCreate, CountryResponse

router = APIRouter(prefix="/api/v1", tags=["Countries"])


@router.post(
    "/countries", response_model=CountryResponse, status_code=status.HTTP_201_CREATED
)
def create_country(
    country_in: CountryCreate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Record a new country in database."""
    # Validación si ya existe el pais.
    country_exist = (
        db.query(CountryModel)
        .filter(CountryModel.country_code == country_in.country_code.upper())
        .first()
    )

    if country_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The country with code '{country_in.country_code.upper()}' already exist.",
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


@router.get(
    "/countries",
    response_model=List[CountryResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("20/minute")
def list_country(request: Request, db: Session = Depends(get_db)):
    countries = db.query(CountryModel).all()

    return countries
