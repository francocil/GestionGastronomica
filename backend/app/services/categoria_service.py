from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from datetime import datetime, timezone


class CategoriaService:

    @staticmethod
    def get(db: Session, categoria_id: int) -> Categoria | None:
        return (
            db.query(Categoria)
            .filter(Categoria.id == categoria_id, Categoria.eliminado == False)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(Categoria).filter(Categoria.eliminado == False).all()

    @staticmethod
    def create(db: Session, data: CategoriaCreate) -> Categoria:
        categoria = Categoria(**data.dict())
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria

    @staticmethod
    def update(db: Session, categoria: Categoria, data: CategoriaUpdate) -> Categoria:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(categoria, field, value)

        categoria.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]

        db.commit()
        db.refresh(categoria)
        return categoria

    @staticmethod
    def soft_delete(db: Session, categoria: Categoria):
        categoria.eliminado = True
        categoria.fecha_actualizacion = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.commit()
        return categoria
