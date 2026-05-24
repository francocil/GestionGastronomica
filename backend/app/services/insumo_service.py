from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.insumo import Insumo
from app.schemas.insumo import (
    InsumoCreate,
    InsumoUpdate,
)


class InsumoService:

    @staticmethod
    def get(db: Session, insumo_id: int) -> Insumo | None:
        return (
            db.query(Insumo)
            .filter(Insumo.id == insumo_id, Insumo.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(Insumo).filter(Insumo.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: InsumoCreate, tenant_id: int) -> Insumo:
        insumo = Insumo(**data.dict(), tenant_id=tenant_id)
        db.add(insumo)
        db.commit()
        db.refresh(insumo)
        return insumo

    @staticmethod
    def update(db: Session, insumo: Insumo, data: InsumoUpdate) -> Insumo:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(insumo, field, value)

        insumo.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(insumo)
        return insumo

    @staticmethod
    def soft_delete(db: Session, insumo: Insumo):
        insumo.eliminado = True
        insumo.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return insumo
