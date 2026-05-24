from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: Optional[bool] = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    eliminado: Optional[bool] = None


class CategoriaInDB(CategoriaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class CategoriaPublic(CategoriaInDB):
    pass
