from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.unidad_medida import (
    UnidadMedidaCreate,
    UnidadMedidaUpdate,
    UnidadMedidaPublic,
)
from app.services.unidad_medida_service import UnidadMedidaService

router = APIRouter(prefix="/unidades-medida", tags=["UnidadMedida"])


@router.get("/", response_model=list[UnidadMedidaPublic])
def listar(db: Session = Depends(get_db)):
    return UnidadMedidaService.get_all(db)


@router.get("/{unidad_id}", response_model=UnidadMedidaPublic)
def obtener(unidad_id: int, db: Session = Depends(get_db)):
    unidad = UnidadMedidaService.get(db, unidad_id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return unidad


@router.post("/", response_model=UnidadMedidaPublic)
def crear(data: UnidadMedidaCreate, db: Session = Depends(get_db)):
    return UnidadMedidaService.create(db, data)


@router.put("/{unidad_id}", response_model=UnidadMedidaPublic)
def actualizar(unidad_id: int, data: UnidadMedidaUpdate, db: Session = Depends(get_db)):
    unidad = UnidadMedidaService.get(db, unidad_id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return UnidadMedidaService.update(db, unidad, data)


@router.delete("/{unidad_id}", response_model=UnidadMedidaPublic)
def eliminar(unidad_id: int, db: Session = Depends(get_db)):
    unidad = UnidadMedidaService.get(db, unidad_id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return UnidadMedidaService.soft_delete(db, unidad)
