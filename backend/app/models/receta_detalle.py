from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.receta import Receta
    from app.models.insumo import Insumo
    from app.models.unidad_medida import UnidadMedida


class RecetaDetalle(Base):
    __tablename__ = "receta_detalle"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)

    receta_id: Mapped[int] = mapped_column(ForeignKey("recetas.id"))
    insumo_id: Mapped[int] = mapped_column(ForeignKey("insumos.id"))
    unidad_medida_id: Mapped[int] = mapped_column(ForeignKey("unidades_medida.id"))

    cantidad: Mapped[float] = mapped_column(nullable=False)
    costo_parcial: Mapped[float] = mapped_column(nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    receta: Mapped["Receta"] = relationship(back_populates="detalles")
    insumo: Mapped["Insumo"] = relationship(back_populates="receta_detalles")
    unidad_medida: Mapped["UnidadMedida"] = relationship()
