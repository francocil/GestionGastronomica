from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class DireccionCliente(Base):
    __tablename__ = "clientes_direcciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

    calle: Mapped[str] = mapped_column(String(150))
    numero: Mapped[str | None] = mapped_column(String(20))
    piso: Mapped[str | None] = mapped_column(String(20))
    dpto: Mapped[str | None] = mapped_column(String(20))

    localidad_id: Mapped[int] = mapped_column(ForeignKey("localidades.id"))
