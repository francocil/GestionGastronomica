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

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.categoria import Categoria
    from app.models.unidad_medida import UnidadMedida
    from app.models.receta import Receta
    from app.models.sucursal import Sucursal


class Product(Base):
    __tablename__ = "products"

    # -------------------------
    # Identificación
    # -------------------------
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),
        index=True,
        nullable=False,
    )

    # -------------------------
    # Relaciones principales
    # -------------------------
    categoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("categorias.id"),
        nullable=True,
    )
    categoria: Mapped["Categoria"] = relationship(back_populates="productos")

    unidad_medida_id: Mapped[int | None] = mapped_column(
        ForeignKey("unidades_medida.id"),
        nullable=True,
    )
    unidad_medida: Mapped["UnidadMedida"] = relationship()

    sucursal_id: Mapped[int | None] = mapped_column(
        ForeignKey("sucursales.id"),
        nullable=True,
    )
    sucursal: Mapped["Sucursal"] = relationship()

    # -------------------------
    # Datos del producto
    # -------------------------
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(300))

    sku: Mapped[str | None] = mapped_column(String(50), index=True)

    precio: Mapped[float] = mapped_column(Float, nullable=False)
    costo: Mapped[float | None] = mapped_column(Float)

    imagen_url: Mapped[str | None] = mapped_column(String(300))

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # -------------------------
    # Auditoría
    # -------------------------
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # -------------------------
    # Relaciones derivadas
    # -------------------------
    receta: Mapped["Receta"] = relationship(
        back_populates="producto",
        uselist=False,
    )
