from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tipo_usuario import (
    TipoUsuarioCreate,
    TipoUsuarioUpdate,
    TipoUsuarioPublic,
)
from app.services.tipo_usuario_service import TipoUsuarioService

router = APIRouter(prefix="/tipo-usuario", tags=["TipoUsuario"])


@router.get("/", response_model=list[TipoUsuarioPublic])
def listar(db: Session = Depends(get_db)):
    return TipoUsuarioService.get_all(db)


@router.get("/{tipo_id}", response_model=TipoUsuarioPublic)
def obtener(tipo_id: int, db: Session = Depends(get_db)):
    tipo = TipoUsuarioService.get(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="TipoUsuario no encontrado")
    return tipo


@router.post("/", response_model=TipoUsuarioPublic)
def crear(data: TipoUsuarioCreate, db: Session = Depends(get_db)):
    return TipoUsuarioService.create(db, data)


@router.put("/{tipo_id}", response_model=TipoUsuarioPublic)
def actualizar(tipo_id: int, data: TipoUsuarioUpdate, db: Session = Depends(get_db)):
    tipo = TipoUsuarioService.get(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="TipoUsuario no encontrado")
    return TipoUsuarioService.update(db, tipo, data)


@router.delete("/{tipo_id}", response_model=TipoUsuarioPublic)
def eliminar(tipo_id: int, db: Session = Depends(get_db)):
    tipo = TipoUsuarioService.get(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="TipoUsuario no encontrado")
    return TipoUsuarioService.soft_delete(db, tipo)
