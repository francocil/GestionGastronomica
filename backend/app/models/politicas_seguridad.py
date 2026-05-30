from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PoliticaSeguridad(Base):
    __tablename__ = "politicas_seguridad"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        nullable=False,
        index=True
    )

    # Password policy
    min_caracteres: Mapped[int] = mapped_column(Integer, default=8)
    requiere_mayuscula: Mapped[bool] = mapped_column(Boolean, default=True)
    requiere_minuscula: Mapped[bool] = mapped_column(Boolean, default=True)
    requiere_numero: Mapped[bool] = mapped_column(Boolean, default=True)
    requiere_simbolo: Mapped[bool] = mapped_column(Boolean, default=False)

    expiracion_dias: Mapped[int] = mapped_column(Integer, default=90)
    intentos_maximos: Mapped[int] = mapped_column(Integer, default=5)

    # MFA
    mfa_obligatorio: Mapped[bool] = mapped_column(Boolean, default=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
