from __future__ import annotations

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MFAEstado(Base):
    __tablename__ = "mfa_estado"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)
