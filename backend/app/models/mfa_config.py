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


class MFAConfig(Base):
    __tablename__ = "mfa_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    usuario: Mapped["User"] = relationship()

    # TOTP secreto (encriptado)
    secret_encrypted: Mapped[str | None] = mapped_column(String(255))

    # Método MFA elegido: TOTP / SMS / EMAIL
    metodo: Mapped[str] = mapped_column(String(20), default="TOTP")

    # Estado MFA
    habilitado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_habilitacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Auditoría
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
