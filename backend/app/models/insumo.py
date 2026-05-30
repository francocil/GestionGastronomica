from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.unidad_medida import UnidadMedida
    from app.models.receta_detalle import RecetaDetalle
    from app.models.stock_movimiento import StockMovimiento
    from app.models.empresa import Empresa


class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
        nullable=False,
    )
    empresa: Mapped["Empresa"] = relationship()

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(300))

    unidad_medida_id: Mapped[int] = mapped_column(ForeignKey("unidades_medida.id"))
    unidad_medida: Mapped["UnidadMedida"] = relationship(back_populates="insumos")

    costo_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    stock_actual: Mapped[float] = mapped_column(default=0)
    stock_minimo: Mapped[float] = mapped_column(default=0)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    receta_detalles: Mapped[list["RecetaDetalle"]] = relationship(back_populates="insumo")
    movimientos: Mapped[list["StockMovimiento"]] = relationship(back_populates="insumo")
