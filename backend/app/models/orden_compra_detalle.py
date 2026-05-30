from __future__ import annotations
from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.orden_compra import OrdenCompra

class OrdenCompraDetalle(Base):
    __tablename__ = "ordenes_compra_detalle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    orden_id: Mapped[int] = mapped_column(ForeignKey("ordenes_compra.id"))
    insumo_id: Mapped[int] = mapped_column(ForeignKey("insumos.id"))

    cantidad: Mapped[float] = mapped_column(Float)
    precio_estimado: Mapped[float] = mapped_column(Float)

    orden: Mapped["OrdenCompra"] = relationship(back_populates="detalles")
