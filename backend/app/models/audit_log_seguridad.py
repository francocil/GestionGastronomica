from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class AuditLogSeguridad(Base):
    __tablename__ = "audit_log_seguridad"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    accion: Mapped[str] = mapped_column(String(100))
    detalle: Mapped[dict | None] = mapped_column(JSON)

    ip: Mapped[str | None] = mapped_column(String(50))
    user_agent: Mapped[str | None] = mapped_column(String(200))

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
