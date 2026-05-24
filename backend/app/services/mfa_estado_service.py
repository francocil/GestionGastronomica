from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.mfa_estado import MFAEstado
from app.schemas.mfa_estado import (
    MFAEstadoCreate,
    MFAEstadoUpdate,
)


class MFAEstadoService:

    @staticmethod
    def get(db: Session, mfa_id: int) -> MFAEstado | None:
        return (
            db.query(MFAEstado)
            .filter(MFAEstado.id == mfa_id, MFAEstado.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(MFAEstado).filter(MFAEstado.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: MFAEstadoCreate) -> MFAEstado:
        mfa = MFAEstado(**data.dict())
        db.add(mfa)
        db.commit()
        db.refresh(mfa)
        return mfa

    @staticmethod
    def update(db: Session, mfa: MFAEstado, data: MFAEstadoUpdate) -> MFAEstado:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(mfa, field, value)

        mfa.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(mfa)
        return mfa

    @staticmethod
    def soft_delete(db: Session, mfa: MFAEstado):
        mfa.eliminado = True
        mfa.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return mfa
