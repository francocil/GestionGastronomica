from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.receta_detalle import RecetaDetalle
from app.schemas.receta_detalle import (
    RecetaDetalleCreate,
    RecetaDetalleUpdate,
)


class RecetaDetalleService:

    @staticmethod
    def get(db: Session, detalle_id: int) -> RecetaDetalle | None:
        return (
            db.query(RecetaDetalle)
            .filter(RecetaDetalle.id == detalle_id, RecetaDetalle.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(RecetaDetalle).filter(RecetaDetalle.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: RecetaDetalleCreate, tenant_id: int) -> RecetaDetalle:
        detalle = RecetaDetalle(**data.dict(), tenant_id=tenant_id)
        db.add(detalle)
        db.commit()
        db.refresh(detalle)
        return detalle

    @staticmethod
    def update(db: Session, detalle: RecetaDetalle, data: RecetaDetalleUpdate) -> RecetaDetalle:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(detalle, field, value)

        detalle.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(detalle)
        return detalle

    @staticmethod
    def soft_delete(db: Session, detalle: RecetaDetalle):
        detalle.eliminado = True
        detalle.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return detalle
