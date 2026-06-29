from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


def init_db():
    """Importación local (Lazy Import) de todos los modelos del proyecto"""
    from app.modules.country.models import CountryModel  # noqa
    from app.modules.holiday.models import HolidayModel  # noqa
    from app.modules.user.models import UserModel  # noqa

    # Crea las tablas si o no existe (ideal para desarrollo inicial)
    base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
