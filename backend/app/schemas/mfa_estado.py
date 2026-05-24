from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MFAEstadoBase(BaseModel):
    nombre: str


class MFAEstadoCreate(MFAEstadoBase):
    pass


class MFAEstadoUpdate(BaseModel):
    nombre: Optional[str] = None
    eliminado: Optional[bool] = None


class MFAEstadoInDB(MFAEstadoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class MFAEstadoPublic(MFAEstadoInDB):
    pass
