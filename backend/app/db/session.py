from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base

# Crear engine con la cadena de conexión real
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Cambiar a True si querés ver SQL en consola
    future=True
)

# Crear SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
