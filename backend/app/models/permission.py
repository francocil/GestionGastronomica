from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.models.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    activo = Column(Boolean, default=True, nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
