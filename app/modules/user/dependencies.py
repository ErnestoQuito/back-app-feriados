# MIDDLEWARE o GUARDIAN
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.modules.user.models import UserModel
from app.modules.user.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str = payload.get("sub", {})
        if not user_id:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    if user.is_active is False:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    return user
