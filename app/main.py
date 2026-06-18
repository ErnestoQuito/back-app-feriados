from fastapi import FastAPI

from app.modules.token.router import router as auth_router

apirest = FastAPI()

apirest.include_router(auth_router)


@apirest.get("/")
async def root() -> dict:
    return {"title": "Feriados Sudamerica"}
