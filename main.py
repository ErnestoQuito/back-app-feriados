from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from slowapi.errors import RateLimitExceeded

from app.core.database import engine, init_db
from app.core.limiter import limiter
from app.modules.country.router import router as country_router
from app.modules.holiday.router import router as holiday_router
from app.modules.user.router import router as auth_router

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

@apirest.get("/favicon.ico", include_in_schema=False)
async def favicon():
    # Obtiene la ruta absoluta del archivo en el contenedor
    favicon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")

    # Si el archivo existe en el contenedor, lo sirve de inmediato
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)

    # Resguardo en caso de que falle, para evitar el error 404 en los logs
    from fastapi import Response
    return Response(status_code=204)

apirest.state.limiter = limiter


def custom_rate_limit_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "message": "Has superado el límite de peticiones permitido. Por favor, espera un momento.",
            "detail": str(
                exc
            ),  # Esto mantendrá el texto de slowapi (ej: "Rate limit exceeded: 5 per 1 minute")
        },
    )


apirest.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

ALLOWED_ORIGINS = ["http://localhost:5173", "http://192.168.31.231:5173"]
apirest.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

apirest.include_router(country_router)
apirest.include_router(holiday_router)
apirest.include_router(auth_router)


@apirest.get("/")
@limiter.limit("20/minute")
async def root(request: Request) -> dict:
    # Si la URL contiene parámetros de consulta (ej. ?rest_route=...), rechazamos la petición
        if request.query_params:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        return {
            "message": "Feriados LATAM API activa",
            "documentation": "/docs"
        }
