from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sucursal import (
    SucursalCreate,
    SucursalUpdate,
    SucursalPublic,
)
from app.services.sucursal_service import SucursalService

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])


@router.get("/", response_model=list[SucursalPublic])
def listar(db: Session = Depends(get_db)):
    return SucursalService.get_all(db)


@router.get("/{sucursal_id}", response_model=SucursalPublic)
def obtener(sucursal_id: int, db: Session = Depends(get_db)):
    sucursal = SucursalService.get(db, sucursal_id)
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal


@router.post("/", response_model=SucursalPublic)
def crear(data: SucursalCreate, request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    return SucursalService.create(db, data, tenant_id)


@router.put("/{sucursal_id}", response_model=SucursalPublic)
def actualizar(sucursal_id: int, data: SucursalUpdate, db: Session = Depends(get_db)):
    sucursal = SucursalService.get(db, sucursal_id)
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return SucursalService.update(db, sucursal, data)


@router.delete("/{sucursal_id}", response_model=SucursalPublic)
def eliminar(sucursal_id: int, db: Session = Depends(get_db)):
    sucursal = SucursalService.get(db, sucursal_id)
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return SucursalService.soft_delete(db, sucursal)
