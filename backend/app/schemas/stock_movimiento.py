from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class StockMovimientoBase(BaseModel):
    insumo_id: int
    sucursal_id: int
    tipo_movimiento: str
    cantidad: float
    motivo: Optional[str] = None
    referencia: Optional[str] = None


class StockMovimientoCreate(StockMovimientoBase):
    pass


class StockMovimientoUpdate(BaseModel):
    insumo_id: Optional[int] = None
    sucursal_id: Optional[int] = None
    tipo_movimiento: Optional[str] = None
    cantidad: Optional[float] = None
    motivo: Optional[str] = None
    referencia: Optional[str] = None
    eliminado: Optional[bool] = None


class StockMovimientoInDB(StockMovimientoBase):
    id: int
    tenant_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class StockMovimientoPublic(StockMovimientoInDB):
    pass
