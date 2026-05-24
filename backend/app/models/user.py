# ================================================
# Modelo de Usuario alineado 1:1 al SRS
# - SQLAlchemy 2.0 (Mapped / mapped_column)
# - Multi‑tenant (empresa_id)
# - IAM enterprise (tipo_usuario_id, estado_usuario_id, mfa_estado_id)
# - Seguridad (intentos, bloqueos, auditoría)
# ================================================
from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_tenant_role import UserTenantRole


class User(Base):
    __tablename__ = "users"

    # Identidad
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # SRS: empresa_id (nullable)
    empresa_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("empresas.id"), nullable=True
    )

    # SRS: username
    username: Mapped[str] = mapped_column(String(150), nullable=False)

    # SRS: email único
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)

    # SRS: password_hash
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # SRS: FK IAM
    tipo_usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tipo_usuario.id"), nullable=False
    )
    estado_usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("estado_usuario.id"), nullable=False
    )
    mfa_estado_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("mfa_estado.id"), nullable=False
    )

    # SRS: seguridad
    intentos_fallidos: Mapped[int] = mapped_column(Integer, default=0)
    fecha_bloqueo: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ultimo_cambio_password: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fecha_ultimo_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # SRS: teléfono
    telefono: Mapped[str | None] = mapped_column(String(50))

    # SRS: auditoría
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relación multi‑tenant
    tenants: Mapped[List["UserTenantRole"]] = relationship(
        back_populates="user"
    )


# Índices EXACTOS del SRS
Index("idx_usuario_email", User.email, unique=True)
Index("idx_usuario_empresa_id", User.empresa_id)
