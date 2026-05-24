from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.insumo import (
    InsumoCreate,
    InsumoUpdate,
    InsumoPublic,
)
from app.services.insumo_service import InsumoService

router = APIRouter(prefix="/insumos", tags=["Insumos"])


@router.get("/", response_model=list[InsumoPublic])
def listar(db: Session = Depends(get_db)):
    return InsumoService.get_all(db)


@router.get("/{insumo_id}", response_model=InsumoPublic)
def obtener(insumo_id: int, db: Session = Depends(get_db)):
    insumo = InsumoService.get(db, insumo_id)
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return insumo


@router.post("/", response_model=InsumoPublic)
def crear(data: InsumoCreate, request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    return InsumoService.create(db, data, tenant_id)


@router.put("/{insumo_id}", response_model=InsumoPublic)
def actualizar(insumo_id: int, data: InsumoUpdate, db: Session = Depends(get_db)):
    insumo = InsumoService.get(db, insumo_id)
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return InsumoService.update(db, insumo, data)


@router.delete("/{insumo_id}", response_model=InsumoPublic)
def eliminar(insumo_id: int, db: Session = Depends(get_db)):
    insumo = InsumoService.get(db, insumo_id)
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return InsumoService.soft_delete(db, insumo)
