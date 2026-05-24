from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.unidad_medida import UnidadMedida
from app.schemas.unidad_medida import (
    UnidadMedidaCreate,
    UnidadMedidaUpdate,
)


class UnidadMedidaService:

    @staticmethod
    def get(db: Session, unidad_id: int) -> UnidadMedida | None:
        return (
            db.query(UnidadMedida)
            .filter(UnidadMedida.id == unidad_id, UnidadMedida.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(UnidadMedida).filter(UnidadMedida.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: UnidadMedidaCreate) -> UnidadMedida:
        unidad = UnidadMedida(**data.dict())
        db.add(unidad)
        db.commit()
        db.refresh(unidad)
        return unidad

    @staticmethod
    def update(db: Session, unidad: UnidadMedida, data: UnidadMedidaUpdate) -> UnidadMedida:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(unidad, field, value)

        unidad.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(unidad)
        return unidad

    @staticmethod
    def soft_delete(db: Session, unidad: UnidadMedida):
        unidad.eliminado = True
        unidad.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return unidad
