# =========================================================================
# Este modelo está diseñado para:
# - Representar roles del sistema (ej: Admin, Gerente, Mozo, Cajero, etc.)
# - Ser compatible con SQLAlchemy 2.0
# - Integrarse con UserTenantRole (que crearemos después)
# - Ser extensible para permisos granulares en fases posteriores
# =========================================================================
from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_tenant_role import UserTenantRole


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    usuarios: Mapped[List["UserTenantRole"]] = relationship(
        back_populates="role"
    )

    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        backref="roles",
        lazy="joined"
    )
