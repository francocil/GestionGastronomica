from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# BASE
# ============================================================

class ProductBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = Field(None, max_length=300)

    sku: Optional[str] = Field(None, max_length=50)

    precio: float
    costo: Optional[float] = None

    imagen_url: Optional[str] = Field(None, max_length=300)

    categoria_id: Optional[int] = None
    unidad_medida_id: Optional[int] = None
    sucursal_id: Optional[int] = None

    activo: Optional[bool] = True


# ============================================================
# CREATE
# ============================================================

class ProductCreate(ProductBase):
    """
    Campos requeridos para crear un producto.
    tenant_id NO se recibe desde el cliente.
    costo NO se recibe si el producto tiene receta (se calcula).
    """
    pass


# ============================================================
# UPDATE
# ============================================================

class ProductUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=300)

    sku: Optional[str] = Field(None, max_length=50)

    precio: Optional[float] = None
    costo: Optional[float] = None

    imagen_url: Optional[str] = Field(None, max_length=300)

    categoria_id: Optional[int] = None
    unidad_medida_id: Optional[int] = None
    sucursal_id: Optional[int] = None

    activo: Optional[bool] = None


# ============================================================
# RESPONSE
# ============================================================

class ProductResponse(ProductBase):
    id: int
    tenant_id: int

    fecha_creacion: datetime
    fecha_actualizacion: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
