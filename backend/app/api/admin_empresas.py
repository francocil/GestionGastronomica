from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaPublic
from app.services.empresa_service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["Empresas"])


@router.get("/", response_model=list[EmpresaPublic])
def list_empresas(db: Session = Depends(get_db)):
    return EmpresaService.get_all(db)


@router.get("/{empresa_id}", response_model=EmpresaPublic)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = EmpresaService.get(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.post("/", response_model=EmpresaPublic)
def create_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    return EmpresaService.create(db, data)


@router.put("/{empresa_id}", response_model=EmpresaPublic)
def update_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    empresa = EmpresaService.get(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return EmpresaService.update(db, empresa, data)


@router.delete("/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = EmpresaService.get(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    EmpresaService.soft_delete(db, empresa)
    return {"detail": "Empresa eliminada"}
