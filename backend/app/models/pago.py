from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    comanda_id: Mapped[int | None] = mapped_column(ForeignKey("comandas.id"))

    monto: Mapped[float] = mapped_column(Float, nullable=False)
    medio: Mapped[str] = mapped_column(String(50))  # EFECTIVO / TARJETA / MP / etc.
    estado: Mapped[str] = mapped_column(String(50))  # PENDIENTE / CONFIRMADO / RECHAZADO

    fecha_pago: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
