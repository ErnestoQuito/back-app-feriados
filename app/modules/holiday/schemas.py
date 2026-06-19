from datetime import datetime

from pydantic import BaseModel


class HolidayDB(BaseModel):
    id: int
    holiday_date: datetime
    holiday_desc: str
