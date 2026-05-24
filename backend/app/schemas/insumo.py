from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class InsumoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    unidad_medida_id: int
    costo_unitario: float
    stock_actual: float
    stock_minimo: float
    activo: bool = True


class InsumoCreate(InsumoBase):
    pass


class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    unidad_medida_id: Optional[int] = None
    costo_unitario: Optional[float] = None
    stock_actual: Optional[float] = None
    stock_minimo: Optional[float] = None
    activo: Optional[bool] = None
    eliminado: Optional[bool] = None


class InsumoInDB(InsumoBase):
    id: int
    tenant_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class InsumoPublic(InsumoInDB):
    pass
