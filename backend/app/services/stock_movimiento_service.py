from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.stock_movimiento import StockMovimiento
from app.schemas.stock_movimiento import (
    StockMovimientoCreate,
    StockMovimientoUpdate,
)


class StockMovimientoService:

    @staticmethod
    def get(db: Session, movimiento_id: int) -> StockMovimiento | None:
        return (
            db.query(StockMovimiento)
            .filter(StockMovimiento.id == movimiento_id, StockMovimiento.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(StockMovimiento).filter(StockMovimiento.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: StockMovimientoCreate, tenant_id: int) -> StockMovimiento:
        movimiento = StockMovimiento(**data.dict(), tenant_id=tenant_id)
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)
        return movimiento

    @staticmethod
    def update(db: Session, movimiento: StockMovimiento, data: StockMovimientoUpdate) -> StockMovimiento:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(movimiento, field, value)

        movimiento.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(movimiento)
        return movimiento

    @staticmethod
    def soft_delete(db: Session, movimiento: StockMovimiento):
        movimiento.eliminado = True
        movimiento.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return movimiento
