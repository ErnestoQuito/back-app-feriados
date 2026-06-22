from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, init_db
from app.modules.country.router import router as country_router
from app.modules.holiday.router import router as holiday_router
from app.modules.token.router import router as auth_router

VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Accion al encender: Inicializar base de datos y verificar tablas
    print("..::[LIFESPAN] Iniciando API: Sincronizando modelos con la BD...")
    init_db()
    # Aqui la aAPI se queda online atendiendo peticiones a los routers
    yield

    # Accion al apagar: libera recursos de forma limpiaa
    print("..::[LIFESPAN] Apagando API: Destruyendo Pool de conexiones...")
    # Corta los sockets abierots de inmediato, liberando a Supabase
    engine.dispose()
    print("..::[LIFESPAN] Servidor cerrando de manera segura.")


apirest = FastAPI(title="API HOLIDAY OF WORLD", version=VERSION, lifespan=lifespan)

apirest.include_router(auth_router)
apirest.include_router(country_router)
apirest.include_router(holiday_router)


@apirest.get("/")
async def root() -> dict:
    return {"title": "Feriados Sudamerica"}
