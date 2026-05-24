from sqlalchemy.orm import Session
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate
from datetime import datetime, timezone


class EmpresaService:

    @staticmethod
    def get(db: Session, empresa_id: int) -> Empresa | None:
        return db.query(Empresa).filter(Empresa.id == empresa_id, Empresa.eliminado == False).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Empresa).filter(Empresa.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: EmpresaCreate) -> Empresa:
        empresa = Empresa(**data.dict())
        db.add(empresa)
        db.commit()
        db.refresh(empresa)
        return empresa

    @staticmethod
    def update(db: Session, empresa: Empresa, data: EmpresaUpdate) -> Empresa:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(empresa, field, value)

        empresa.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(empresa)
        return empresa

    @staticmethod
    def soft_delete(db: Session, empresa: Empresa):
        empresa.eliminado = True
        empresa.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return empresa
