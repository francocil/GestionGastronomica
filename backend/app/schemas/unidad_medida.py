from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UnidadMedidaBase(BaseModel):
    nombre: str
    abreviatura: str


class UnidadMedidaCreate(UnidadMedidaBase):
    pass


class UnidadMedidaUpdate(BaseModel):
    nombre: Optional[str] = None
    abreviatura: Optional[str] = None
    activo: Optional[bool] = None
    eliminado: Optional[bool] = None


class UnidadMedidaInDB(UnidadMedidaBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class UnidadMedidaPublic(UnidadMedidaInDB):
    pass
