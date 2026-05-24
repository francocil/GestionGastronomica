from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.receta_detalle import (
    RecetaDetalleCreate,
    RecetaDetalleUpdate,
    RecetaDetallePublic,
)
from app.services.receta_detalle_service import RecetaDetalleService

router = APIRouter(prefix="/receta-detalle", tags=["RecetaDetalle"])


@router.get("/", response_model=list[RecetaDetallePublic])
def listar(db: Session = Depends(get_db)):
    return RecetaDetalleService.get_all(db)


@router.get("/{detalle_id}", response_model=RecetaDetallePublic)
def obtener(detalle_id: int, db: Session = Depends(get_db)):
    detalle = RecetaDetalleService.get(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.post("/", response_model=RecetaDetallePublic)
def crear(data: RecetaDetalleCreate, request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    return RecetaDetalleService.create(db, data, tenant_id)


@router.put("/{detalle_id}", response_model=RecetaDetallePublic)
def actualizar(detalle_id: int, data: RecetaDetalleUpdate, db: Session = Depends(get_db)):
    detalle = RecetaDetalleService.get(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return RecetaDetalleService.update(db, detalle, data)


@router.delete("/{detalle_id}", response_model=RecetaDetallePublic)
def eliminar(detalle_id: int, db: Session = Depends(get_db)):
    detalle = RecetaDetalleService.get(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return RecetaDetalleService.soft_delete(db, detalle)
