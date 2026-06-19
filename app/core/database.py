from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = environ.get("DATABASE_URL", None)

if not DATABASE_URL:
    raise Exception(
        "..:: the database variable not found. Please, check your configuration."
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


def init_db():
    """Importación local (Lazy Import) de todos los modelos del proyecto"""
    from app.modules.country.models import CountryModel

    # Crea las tablas si o no existe (ideal para desarrollo inicial)
    base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
