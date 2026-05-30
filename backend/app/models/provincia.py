from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Provincia(Base):
    __tablename__ = "provincias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pais_id: Mapped[int] = mapped_column(ForeignKey("paises.id"), nullable=False)

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
