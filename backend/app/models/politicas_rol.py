from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class PoliticaRol(Base):
    __tablename__ = "politicas_rol"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    permiso_id: Mapped[int] = mapped_column(ForeignKey("permisos.id"))

    permitido: Mapped[bool] = mapped_column(Boolean, default=True)
