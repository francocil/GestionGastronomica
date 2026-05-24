from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TipoUsuarioBase(BaseModel):
    nombre: str


class TipoUsuarioCreate(TipoUsuarioBase):
    pass


class TipoUsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    eliminado: Optional[bool] = None


class TipoUsuarioInDB(TipoUsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class TipoUsuarioPublic(TipoUsuarioInDB):
    pass
