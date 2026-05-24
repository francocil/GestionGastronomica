from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RecetaDetalleBase(BaseModel):
    receta_id: int
    insumo_id: int
    unidad_medida_id: int
    cantidad: float
    costo_parcial: float


class RecetaDetalleCreate(RecetaDetalleBase):
    pass


class RecetaDetalleUpdate(BaseModel):
    receta_id: Optional[int] = None
    insumo_id: Optional[int] = None
    unidad_medida_id: Optional[int] = None
    cantidad: Optional[float] = None
    costo_parcial: Optional[float] = None
    eliminado: Optional[bool] = None


class RecetaDetalleInDB(RecetaDetalleBase):
    id: int
    tenant_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class RecetaDetallePublic(RecetaDetalleInDB):
    pass
