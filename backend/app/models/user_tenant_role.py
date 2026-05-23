# =============================================================================================
# Este modelo representa la relación pivot entre:
# - Un usuario (User)
# - Una empresa (Tenant)
# - Un rol asignado dentro de esa empresa (Role)
#
# Su propósito es:
# - Implementar multi‑tenant real, permitiendo que un usuario pertenezca a múltiples empresas.
# - Permitir que un usuario tenga distintos roles según el tenant.
# - Mantener compatibilidad con SQLAlchemy 2.0.
# - Incluir auditoría estándar para trazabilidad.
# - Servir como base para el sistema de permisos y autenticación IAM.
# =============================================================================================
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.tenant import Tenant
    from app.models.role import Role


class UserTenantRole(Base):
    __tablename__ = "user_tenant_role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="tenants")
    tenant: Mapped["Tenant"] = relationship(back_populates="usuarios")
    role: Mapped["Role"] = relationship(back_populates="usuarios")

    __table_args__ = (
        UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),
    )
