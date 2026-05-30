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
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.categoria import CategoriaProducto
    from app.models.unidad_medida import UnidadMedida
    from app.models.receta import Receta
    from app.models.empresa import Empresa


class Product(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
        nullable=False,
    )
    empresa: Mapped["Empresa"] = relationship()

    categoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("categorias_producto.id"),
        nullable=True,
    )
    categoria: Mapped["CategoriaProducto"] = relationship(back_populates="productos")

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(300))

    sku: Mapped[str | None] = mapped_column(String(50), index=True)

    precio: Mapped[float] = mapped_column(Float, nullable=False)
    costo: Mapped[float | None] = mapped_column(Float)

    moneda_id: Mapped[int | None] = mapped_column(ForeignKey("monedas.id"))

    imagen_url: Mapped[str | None] = mapped_column(String(300))

    tiempo_preparacion: Mapped[int | None] = mapped_column(Integer)

    es_combo: Mapped[bool] = mapped_column(Boolean, default=False)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True)

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
    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    receta: Mapped["Receta"] = relationship(
        back_populates="producto",
        uselist=False,
    )
