from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class SucursalBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    activo: bool = True


class SucursalCreate(SucursalBase):
    pass


class SucursalUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    eliminado: Optional[bool] = None


class SucursalInDB(SucursalBase):
    id: int
    tenant_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class SucursalPublic(SucursalInDB):
    pass
