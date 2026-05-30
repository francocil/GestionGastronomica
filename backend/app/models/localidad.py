from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Localidad(Base):
    __tablename__ = "localidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincias.id"), nullable=False)

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
