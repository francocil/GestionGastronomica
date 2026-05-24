from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.receta import (
    RecetaCreate,
    RecetaUpdate,
    RecetaPublic,
)
from app.services.receta_service import RecetaService

router = APIRouter(prefix="/recetas", tags=["Recetas"])


@router.get("/", response_model=list[RecetaPublic])
def listar(db: Session = Depends(get_db)):
    return RecetaService.get_all(db)


@router.get("/{receta_id}", response_model=RecetaPublic)
def obtener(receta_id: int, db: Session = Depends(get_db)):
    receta = RecetaService.get(db, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta


@router.post("/", response_model=RecetaPublic)
def crear(data: RecetaCreate, request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    return RecetaService.create(db, data, tenant_id)


@router.put("/{receta_id}", response_model=RecetaPublic)
def actualizar(receta_id: int, data: RecetaUpdate, db: Session = Depends(get_db)):
    receta = RecetaService.get(db, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return RecetaService.update(db, receta, data)


@router.delete("/{receta_id}", response_model=RecetaPublic)
def eliminar(receta_id: int, db: Session = Depends(get_db)):
    receta = RecetaService.get(db, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return RecetaService.soft_delete(db, receta)
