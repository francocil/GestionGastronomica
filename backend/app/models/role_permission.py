# role_permission.py
from datetime import datetime

from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime,
    func,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RolPermiso(Base):
    __tablename__ = "roles_permisos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    rol_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )
    permiso_id: Mapped[int] = mapped_column(
        ForeignKey("permisos.id", ondelete="CASCADE"),
        nullable=False,
    )

    permitido: Mapped[bool] = mapped_column(Boolean, default=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
