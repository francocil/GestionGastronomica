from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class TrackingEntrega(Base):
    __tablename__ = "tracking_entrega"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    entrega_id: Mapped[int] = mapped_column(ForeignKey("entregas.id"))

    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
