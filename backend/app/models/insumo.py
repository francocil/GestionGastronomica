from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.unidad_medida import UnidadMedida
    from app.models.receta_detalle import RecetaDetalle
    from app.models.stock_movimiento import StockMovimiento


class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(300))

    unidad_medida_id: Mapped[int] = mapped_column(ForeignKey("unidades_medida.id"))
    unidad_medida: Mapped["UnidadMedida"] = relationship(back_populates="insumos")

    costo_unitario: Mapped[float] = mapped_column(nullable=False)

    stock_actual: Mapped[float] = mapped_column(default=0)
    stock_minimo: Mapped[float] = mapped_column(default=0)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    receta_detalles: Mapped[list["RecetaDetalle"]] = relationship(
        back_populates="insumo"
    )
    movimientos: Mapped[list["StockMovimiento"]] = relationship(
        back_populates="insumo"
    )
