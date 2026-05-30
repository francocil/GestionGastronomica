# permission.py
from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.role import Rol


class Permission(Base):
    __tablename__ = "permisos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    codigo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255))

    categoria_id: Mapped[int | None] = mapped_column(ForeignKey("permisos_categoria.id"))

    es_critico: Mapped[bool] = mapped_column(Boolean, default=False)
    requiere_mfa: Mapped[bool] = mapped_column(Boolean, default=False)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    roles: Mapped[List["Rol"]] = relationship(
        secondary="roles_permisos",
        back_populates="permisos",
    )
