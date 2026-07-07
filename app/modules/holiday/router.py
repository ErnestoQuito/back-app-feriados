from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.user.dependencies import get_current_user
from app.modules.user.models import UserModel
from main import limiter

from .models import HolidayModel
from .schemas import HolidayCreate, HolidayResponse

router = APIRouter(prefix="/api/v1", tags=["Holidays"])


@router.post(
    "/holidays", response_model=HolidayResponse, status_code=status.HTTP_201_CREATED
)
def create_holiday(
    holiday_in: HolidayCreate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    "Record a new holiday in database"
    # Validar si existe el día festivo.
    holiday_exist = (
        db.query(HolidayModel)
        .filter(
            HolidayModel.holiday_name == holiday_in.holiday_name,
            HolidayModel.holiday_date == holiday_in.holiday_date,
        )
        .first()
    )

    if holiday_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The holiday with name '{holiday_in.holiday_name}' already exist.",
        )

    # De modelo Pydantic a modleo SqlAlchemy
    holiday_new = HolidayModel(
        holiday_date=holiday_in.holiday_date,
        holiday_name=holiday_in.holiday_name,
        holiday_description=holiday_in.holiday_description,
        holiday_type=holiday_in.holiday_type,
        holiday_is_substitutable=holiday_in.holiday_is_substitutable,
        holiday_is_mandatory=holiday_in.holiday_is_mandatory,
        holiday_law_reference=holiday_in.holiday_law_reference,
        id_country=holiday_in.id_country,
    )
    db.add(holiday_new)
    db.commit()
    db.refresh(holiday_new)

    return holiday_new


@router.get(
    "/holidays/{id_country}",
    response_model=list[HolidayResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("20/minute")
def get_holidays_by_country(id_country: int, db: Session = Depends(get_db)):
    holidays = (
        db.query(HolidayModel)
        .filter(HolidayModel.id_country == id_country)
        .order_by(HolidayModel.holiday_date.asc())
        .all()
    )

    if not holidays:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron días festivos para el pais.",
        )
    return holidays
