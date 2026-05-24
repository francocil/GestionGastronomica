from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.estado_usuario import EstadoUsuario
from app.schemas.estado_usuario import (
    EstadoUsuarioCreate,
    EstadoUsuarioUpdate,
)


class EstadoUsuarioService:

    @staticmethod
    def get(db: Session, estado_id: int) -> EstadoUsuario | None:
        return (
            db.query(EstadoUsuario)
            .filter(EstadoUsuario.id == estado_id, EstadoUsuario.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(EstadoUsuario).filter(EstadoUsuario.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: EstadoUsuarioCreate) -> EstadoUsuario:
        estado = EstadoUsuario(**data.dict())
        db.add(estado)
        db.commit()
        db.refresh(estado)
        return estado

    @staticmethod
    def update(db: Session, estado: EstadoUsuario, data: EstadoUsuarioUpdate) -> EstadoUsuario:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(estado, field, value)

        estado.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(estado)
        return estado

    @staticmethod
    def soft_delete(db: Session, estado: EstadoUsuario):
        estado.eliminado = True
        estado.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return estado
