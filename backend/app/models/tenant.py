# =====================================================================================================
# Este modelo está diseñado para:
# - Representar una empresa (tenant) dentro del sistema multi‑tenant.
# - Ser compatible con SQLAlchemy 2.0 usando DeclarativeBase.
# - Integrarse con el modelo UserTenantRole para asignar usuarios y roles por empresa.
# - Permitir aislamiento de datos entre diferentes organizaciones.
# - Ser extensible para futuras fases (datos fiscales, configuración de facturación, sucursales, etc.).
# - Incluir auditoría estándar mediante fecha_creacion y fecha_actualizacion.
# =====================================================================================================
from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_tenant_role import UserTenantRole
    from app.models.product import Product


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    razon_social: Mapped[str | None] = mapped_column(String(200))
    cuit: Mapped[str | None] = mapped_column(String(20), unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relación con usuarios asignados al tenant
    usuarios: Mapped[List["UserTenantRole"]] = relationship(
        back_populates="tenant"
    )

    # Relación con productos del tenant (Fase 2)
    productos: Mapped[List["Product"]] = relationship(
        back_populates="tenant"
    )
