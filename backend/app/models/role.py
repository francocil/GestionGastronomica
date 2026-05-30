from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_tenant_role import UsuarioRol
    from app.models.permission import Permission


class Rol(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255))

    nivel_id: Mapped[int] = mapped_column(ForeignKey("roles_nivel.id"))
    codigo: Mapped[str] = mapped_column(String(100), unique=True)

    es_sistema: Mapped[bool] = mapped_column(Boolean, default=False)
    prioridad: Mapped[int | None] = mapped_column(Integer)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    usuarios: Mapped[List["UsuarioRol"]] = relationship(
        back_populates="rol"
    )

    permisos: Mapped[List["Permission"]] = relationship(
        secondary="roles_permisos",
        back_populates="roles",
        lazy="joined",
    )
