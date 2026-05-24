from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaPublic,
)
from app.services.categoria_service import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=list[CategoriaPublic])
def list_categorias(db: Session = Depends(get_db)):
    return CategoriaService.get_all(db)


@router.get("/{categoria_id}", response_model=CategoriaPublic)
def get_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = CategoriaService.get(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post("/", response_model=CategoriaPublic)
def create_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):
    return CategoriaService.create(db, data)


@router.put("/{categoria_id}", response_model=CategoriaPublic)
def update_categoria(categoria_id: int, data: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = CategoriaService.get(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return CategoriaService.update(db, categoria, data)


@router.delete("/{categoria_id}")
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = CategoriaService.get(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    CategoriaService.soft_delete(db, categoria)
    return {"detail": "Categoría eliminada"}
