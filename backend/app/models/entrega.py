from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Entrega(Base):
    __tablename__ = "entregas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    comanda_id: Mapped[int] = mapped_column(ForeignKey("comandas.id"))
    repartidor_id: Mapped[int] = mapped_column(ForeignKey("repartidores.id"))

    estado: Mapped[str] = mapped_column(String(50))  # ASIGNADA / EN_CAMINO / ENTREGADA

    fecha_asignacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
