from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.orden_compra_detalle import OrdenCompraDetalle

class OrdenCompra(Base):
    __tablename__ = "ordenes_compra"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    proveedor: Mapped[str] = mapped_column(String(150))

    estado: Mapped[str] = mapped_column(String(50))  # BORRADOR / ENVIADA / APROBADA / RECIBIDA

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    detalles: Mapped[list["OrdenCompraDetalle"]] = relationship(back_populates="orden")
