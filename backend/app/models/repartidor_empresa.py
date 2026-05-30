from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class RepartidorEmpresa(Base):
    __tablename__ = "repartidor_empresa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    repartidor_id: Mapped[int] = mapped_column(ForeignKey("repartidores.id"))
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))

    prioridad: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("repartidor_id", "empresa_id", name="uq_repartidor_empresa"),
    )
