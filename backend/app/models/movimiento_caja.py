from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class MovimientoCaja(Base):
    __tablename__ = "movimientos_caja"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    caja_id: Mapped[int] = mapped_column(ForeignKey("cajas.id"))

    tipo: Mapped[str] = mapped_column(String(20))  # INGRESO / EGRESO
    categoria: Mapped[str] = mapped_column(String(50))  # VENTA / GASTO / AJUSTE

    monto: Mapped[float] = mapped_column(Float)

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
