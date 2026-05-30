from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    Integer,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.stock_movimiento import StockMovimiento
    from app.models.empresa import Empresa


class Sucursal(Base):
    __tablename__ = "sucursales"

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
        nullable=False,
    )
    empresa: Mapped["Empresa"] = relationship()

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)

    # Dirección detallada
    localidad_id: Mapped[int | None] = mapped_column(ForeignKey("localidades.id"))
    calle: Mapped[str | None] = mapped_column(String(150))
    numero_calle: Mapped[str | None] = mapped_column(String(20))
    piso: Mapped[str | None] = mapped_column(String(20))
    dpto: Mapped[str | None] = mapped_column(String(20))
    entre_calle1: Mapped[str | None] = mapped_column(String(150))
    entre_calle2: Mapped[str | None] = mapped_column(String(150))

    telefono: Mapped[str | None] = mapped_column(String(50))
    whatsapp: Mapped[str | None] = mapped_column(String(50))

    # Horarios
    horario_apertura: Mapped[str | None] = mapped_column(String(5))   # hh:mm
    horario_cierre: Mapped[str | None] = mapped_column(String(5))     # hh:mm

    # Delivery
    zona_delivery: Mapped[str | None] = mapped_column(String(500))  # radio/polígono (JSON/string)

    # Geo
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)

    # Capacidad operativa
    capacidad_operativa: Mapped[int | None] = mapped_column(Integer)
    tiempo_preparacion_promedio: Mapped[int | None] = mapped_column(Integer)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    movimientos: Mapped[list["StockMovimiento"]] = relationship(
        back_populates="sucursal"
    )
