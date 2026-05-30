from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Moneda(Base):
    __tablename__ = "monedas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    abreviatura: Mapped[str] = mapped_column(String(10), nullable=False)  # ARS, USD
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
