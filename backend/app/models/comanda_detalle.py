from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.comanda import Comanda

class ComandaDetalle(Base):
    __tablename__ = "comanda_detalle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    comanda_id: Mapped[int] = mapped_column(ForeignKey("comandas.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))

    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    comanda: Mapped["Comanda"] = relationship(back_populates="detalles")
