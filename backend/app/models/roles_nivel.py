from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class RolNivel(Base):
    __tablename__ = "roles_nivel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # GLOBAL / EMPRESA / OPERATIVO
