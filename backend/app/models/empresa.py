from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    Index,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Empresa(Base):
    __tablename__ = "empresas"

    __table_args__ = (
        Index("idx_empresa_cuit_cuil", "cuit_cuil", unique=True),
        Index("idx_empresa_activo", "activo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    cuit_cuil: Mapped[str] = mapped_column(String(20), nullable=False)
    razon_social: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre_fantasia: Mapped[str | None] = mapped_column(String(255))

    direccion_fiscal: Mapped[str | None] = mapped_column(String(255))
    email_contacto: Mapped[str | None] = mapped_column(String(150))
    telefono_contacto: Mapped[str | None] = mapped_column(String(50))

    # Geografía
    localidad_id: Mapped[int | None] = mapped_column(ForeignKey("localidades.id"))

    # Estado
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Configuraciones
    configuracion_fiscal_id: Mapped[int | None] = mapped_column(Integer)
    configuracion_delivery_id: Mapped[int | None] = mapped_column(Integer)

    # Auditoría
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)

    # Branding / zona horaria
    logo_url: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[str | None] = mapped_column(String(100))

    # Fiscal / monetario
    moneda_id: Mapped[int | None] = mapped_column(ForeignKey("monedas.id"))
    condicion_iva: Mapped[str | None] = mapped_column(String(50))
    ingresos_brutos: Mapped[str | None] = mapped_column(String(50))

    # SaaS
    plan_suscripcion_id: Mapped[int | None] = mapped_column(Integer)
