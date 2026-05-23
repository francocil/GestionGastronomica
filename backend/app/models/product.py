# =============================================================================================
# Modelo Product
#
# Este modelo representa un producto dentro del sistema gastronómico.
# Está diseñado para:
# - Ser multi‑tenant (cada producto pertenece a un tenant).
# - Ser compatible con SQLAlchemy 2.0.
# - Incluir auditoría estándar.
# - Ser extensible para futuras fases (categorías, variantes, stock, recetas, etc.).
# =============================================================================================

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant


class Product(Base):
    __tablename__ = "products"

    # Identificador único
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Multi‑tenant: cada producto pertenece a un tenant
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)

    # Datos principales del producto
    nombre: Mapped[str] = mapped_column(String(150), index=True)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    precio: Mapped[float] = mapped_column()
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Auditoría
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relación con Tenant
    tenant: Mapped["Tenant"] = relationship(back_populates="productos")
