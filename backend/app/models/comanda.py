from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.comanda_detalle import ComandaDetalle

class Comanda(Base):
    __tablename__ = "comandas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursales.id"))
    cliente_id: Mapped[int | None] = mapped_column(ForeignKey("clientes.id"))

    estado: Mapped[str] = mapped_column(String(50))  # RECIBIDA / EN_COCINA / LISTA / ENTREGADA

    total: Mapped[float] = mapped_column(Float, default=0)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    detalles: Mapped[list["ComandaDetalle"]] = relationship(back_populates="comanda")
