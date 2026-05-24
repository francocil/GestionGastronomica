from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RecetaBase(BaseModel):
    producto_id: int
    descripcion: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    activo: bool = True


class RecetaCreate(RecetaBase):
    pass


class RecetaUpdate(BaseModel):
    producto_id: Optional[int] = None
    descripcion: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    activo: Optional[bool] = None
    eliminado: Optional[bool] = None


class RecetaInDB(RecetaBase):
    id: int
    tenant_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class RecetaPublic(RecetaInDB):
    pass
