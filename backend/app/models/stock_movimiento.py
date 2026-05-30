from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, func, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.insumo import Insumo
    from app.models.sucursal import Sucursal
    from app.models.empresa import Empresa


class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
        nullable=False,
    )

    insumo_id: Mapped[int] = mapped_column(ForeignKey("insumos.id"))
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursales.id"))

    tipo: Mapped[str] = mapped_column(String(20))  # INGRESO / EGRESO / AJUSTE
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    referencia: Mapped[str | None] = mapped_column(String(100))
    motivo: Mapped[str | None] = mapped_column(String(200))

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    insumo: Mapped["Insumo"] = relationship(back_populates="movimientos")
    sucursal: Mapped["Sucursal"] = relationship(back_populates="movimientos")
