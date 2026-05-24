from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.receta import Receta
from app.schemas.receta import (
    RecetaCreate,
    RecetaUpdate,
)


class RecetaService:

    @staticmethod
    def get(db: Session, receta_id: int) -> Receta | None:
        return (
            db.query(Receta)
            .filter(Receta.id == receta_id, Receta.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(Receta).filter(Receta.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: RecetaCreate, tenant_id: int) -> Receta:
        receta = Receta(**data.dict(), tenant_id=tenant_id)
        db.add(receta)
        db.commit()
        db.refresh(receta)
        return receta

    @staticmethod
    def update(db: Session, receta: Receta, data: RecetaUpdate) -> Receta:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(receta, field, value)

        receta.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(receta)
        return receta

    @staticmethod
    def soft_delete(db: Session, receta: Receta):
        receta.eliminado = True
        receta.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return receta
