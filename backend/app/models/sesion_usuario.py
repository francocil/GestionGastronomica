from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.user import User


class SesionUsuario(Base):
    __tablename__ = "sesiones_usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Usuario dueño de la sesión
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    usuario: Mapped["User"] = relationship()

    # Refresh token hasheado (NUNCA en texto plano)
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Datos del dispositivo
    ip: Mapped[str | None] = mapped_column(String(50))
    user_agent: Mapped[str | None] = mapped_column(String(300))
    device_name: Mapped[str | None] = mapped_column(String(150))
    device_type: Mapped[str | None] = mapped_column(String(50))
    ubicacion_aproximada: Mapped[str | None] = mapped_column(String(150))

    # Estado de la sesión
    revocado: Mapped[bool] = mapped_column(Boolean, default=False)
    motivo_revocacion: Mapped[str | None] = mapped_column(String(200))

    # Fechas
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    fecha_expiracion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    ultimo_uso: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
