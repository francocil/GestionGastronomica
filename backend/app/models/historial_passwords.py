from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class HistorialPassword(Base):
    __tablename__ = "historial_passwords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
