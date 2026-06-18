from datetime import datetime

from pydantic import BaseModel


class TokenDB(BaseModel):
    token: str
    created_at: datetime
    expires_at: datetime


class TokenOut(BaseModel):
    token: str
    expires_in: int
