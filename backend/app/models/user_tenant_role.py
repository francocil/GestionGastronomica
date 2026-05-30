# user_tenant_role.py -> UsuarioRol
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.empresa import Empresa
    from app.models.role import Rol
    from app.models.sucursal import Sucursal


class UsuarioRol(Base):
    __tablename__ = "usuarios_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    sucursal_id: Mapped[int | None] = mapped_column(ForeignKey("sucursales.id"))

    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    fecha_asignacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    asignado_por: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    usuario: Mapped["User"] = relationship(foreign_keys=[usuario_id])
    empresa: Mapped["Empresa"] = relationship()
    sucursal: Mapped["Sucursal"] = relationship()
    rol: Mapped["Rol"] = relationship(back_populates="usuarios")

    __table_args__ = (
        UniqueConstraint("usuario_id", "empresa_id", "sucursal_id", "rol_id", name="uq_usuario_empresa_sucursal_rol"),
    )
