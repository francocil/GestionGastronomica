from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.empresa import Empresa


class CategoriaProducto(Base):
    __tablename__ = "categorias_producto"

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
        nullable=False,
    )
    empresa: Mapped["Empresa"] = relationship()

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(300))

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

    productos: Mapped[list["Product"]] = relationship(back_populates="categoria")
