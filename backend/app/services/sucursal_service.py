from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.sucursal import Sucursal
from app.schemas.sucursal import (
    SucursalCreate,
    SucursalUpdate,
)


class SucursalService:

    @staticmethod
    def get(db: Session, sucursal_id: int) -> Sucursal | None:
        return (
            db.query(Sucursal)
            .filter(Sucursal.id == sucursal_id, Sucursal.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(Sucursal).filter(Sucursal.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: SucursalCreate, tenant_id: int) -> Sucursal:
        sucursal = Sucursal(**data.dict(), tenant_id=tenant_id)
        db.add(sucursal)
        db.commit()
        db.refresh(sucursal)
        return sucursal

    @staticmethod
    def update(db: Session, sucursal: Sucursal, data: SucursalUpdate) -> Sucursal:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(sucursal, field, value)

        sucursal.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(sucursal)
        return sucursal

    @staticmethod
    def soft_delete(db: Session, sucursal: Sucursal):
        sucursal.eliminado = True
        sucursal.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return sucursal
