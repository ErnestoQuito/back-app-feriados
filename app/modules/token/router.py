from fastapi import APIRouter

from .schemas import TokenOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/token")
async def token_out() -> TokenOut:
    token_out = TokenOut(token="sfasdyfasdfuashd", expires_in=360)
    return token_out
