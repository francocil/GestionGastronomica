from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class AlertaSeguridad(Base):
    __tablename__ = "alertas_seguridad"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    tipo: Mapped[str] = mapped_column(String(100))  # ej: "attack_detected"
    detalle: Mapped[str | None] = mapped_column(String(500))

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
