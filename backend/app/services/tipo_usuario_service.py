from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.tipo_usuario import TipoUsuario
from app.schemas.tipo_usuario import (
    TipoUsuarioCreate,
    TipoUsuarioUpdate,
)


class TipoUsuarioService:

    @staticmethod
    def get(db: Session, tipo_id: int) -> TipoUsuario | None:
        return (
            db.query(TipoUsuario)
            .filter(TipoUsuario.id == tipo_id, TipoUsuario.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(TipoUsuario).filter(TipoUsuario.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: TipoUsuarioCreate) -> TipoUsuario:
        tipo = TipoUsuario(**data.dict())
        db.add(tipo)
        db.commit()
        db.refresh(tipo)
        return tipo

    @staticmethod
    def update(db: Session, tipo: TipoUsuario, data: TipoUsuarioUpdate) -> TipoUsuario:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(tipo, field, value)

        tipo.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(tipo)
        return tipo

    @staticmethod
    def soft_delete(db: Session, tipo: TipoUsuario):
        tipo.eliminado = True
        tipo.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return tipo
