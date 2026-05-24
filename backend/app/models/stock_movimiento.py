from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.insumo import Insumo
    from app.models.sucursal import Sucursal


class StockMovimiento(Base):
    __tablename__ = "stock_movimientos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)

    insumo_id: Mapped[int] = mapped_column(ForeignKey("insumos.id"))
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursales.id"))

    tipo_movimiento: Mapped[str] = mapped_column(String(20))  # entrada/salida/ajuste
    cantidad: Mapped[float] = mapped_column(nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(200))
    referencia: Mapped[str | None] = mapped_column(String(100))

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

    insumo: Mapped["Insumo"] = relationship(back_populates="movimientos")
    sucursal: Mapped["Sucursal"] = relationship(back_populates="movimientos")
