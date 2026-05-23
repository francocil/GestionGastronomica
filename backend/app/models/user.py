# ================================================
# Este modelo está diseñado para:
# - Autenticación real (email + password hash)
# - Multi‑tenant (relación con UserTenantRole)
# - Auditoría (fechas de creación/actualización)
# - Ser compatible con SQLAlchemy 2.0 
# ================================================
from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_tenant_role import UserTenantRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150))
    apellido: Mapped[str] = mapped_column(String(150))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    tenants: Mapped[List["UserTenantRole"]] = relationship(
        back_populates="user"
    )
