from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, func, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.receta_detalle import RecetaDetalle


class Receta(Base):
    __tablename__ = "recetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)

    producto_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(300))

    tiempo_preparacion: Mapped[int | None] = mapped_column(Integer)

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

    producto: Mapped["Product"] = relationship(back_populates="receta")
    detalles: Mapped[list["RecetaDetalle"]] = relationship(back_populates="receta")
