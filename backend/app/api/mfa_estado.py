from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.mfa_estado import (
    MFAEstadoCreate,
    MFAEstadoUpdate,
    MFAEstadoPublic,
)
from app.services.mfa_estado_service import MFAEstadoService

router = APIRouter(prefix="/mfa-estado", tags=["MFAEstado"])


@router.get("/", response_model=list[MFAEstadoPublic])
def listar(db: Session = Depends(get_db)):
    return MFAEstadoService.get_all(db)


@router.get("/{mfa_id}", response_model=MFAEstadoPublic)
def obtener(mfa_id: int, db: Session = Depends(get_db)):
    mfa = MFAEstadoService.get(db, mfa_id)
    if not mfa:
        raise HTTPException(status_code=404, detail="MFAEstado no encontrado")
    return mfa


@router.post("/", response_model=MFAEstadoPublic)
def crear(data: MFAEstadoCreate, db: Session = Depends(get_db)):
    return MFAEstadoService.create(db, data)


@router.put("/{mfa_id}", response_model=MFAEstadoPublic)
def actualizar(mfa_id: int, data: MFAEstadoUpdate, db: Session = Depends(get_db)):
    mfa = MFAEstadoService.get(db, mfa_id)
    if not mfa:
        raise HTTPException(status_code=404, detail="MFAEstado no encontrado")
    return MFAEstadoService.update(db, mfa, data)


@router.delete("/{mfa_id}", response_model=MFAEstadoPublic)
def eliminar(mfa_id: int, db: Session = Depends(get_db)):
    mfa = MFAEstadoService.get(db, mfa_id)
    if not mfa:
        raise HTTPException(status_code=404, detail="MFAEstado no encontrado")
    return MFAEstadoService.soft_delete(db, mfa)
