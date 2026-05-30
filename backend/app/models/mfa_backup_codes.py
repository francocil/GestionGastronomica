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
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class BackupCode(Base):
    __tablename__ = "mfa_backup_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Código hasheado (NUNCA en texto plano)
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    usado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_uso: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
