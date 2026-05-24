from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class EstadoUsuarioBase(BaseModel):
    nombre: str


class EstadoUsuarioCreate(EstadoUsuarioBase):
    pass


class EstadoUsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    eliminado: Optional[bool] = None


class EstadoUsuarioInDB(EstadoUsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class EstadoUsuarioPublic(EstadoUsuarioInDB):
    pass
