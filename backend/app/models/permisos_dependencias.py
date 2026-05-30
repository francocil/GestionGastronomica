from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class PermisoDependencia(Base):
    __tablename__ = "permisos_dependencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    permiso_id: Mapped[int] = mapped_column(ForeignKey("permisos.id"))
    permiso_requerido_id: Mapped[int] = mapped_column(ForeignKey("permisos.id"))
