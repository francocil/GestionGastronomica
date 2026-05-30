from __future__ import annotations
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class PoliticaAcceso(Base):
    __tablename__ = "politicas_acceso"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))

    recurso: Mapped[str] = mapped_column(String(100))     # ej: "comanda"
    accion: Mapped[str] = mapped_column(String(100))      # ej: "editar"

    condicion_json: Mapped[str] = mapped_column(String(2000))  # JSON ABAC
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
