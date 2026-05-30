from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Caja(Base):
    __tablename__ = "cajas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursales.id"))

    monto_inicial: Mapped[float] = mapped_column(Float)
    abierta_por: Mapped[int] = mapped_column(ForeignKey("users.id"))

    fecha_apertura: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
