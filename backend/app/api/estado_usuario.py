from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.estado_usuario import (
    EstadoUsuarioCreate,
    EstadoUsuarioUpdate,
    EstadoUsuarioPublic,
)
from app.services.estado_usuario_service import EstadoUsuarioService

router = APIRouter(prefix="/estado-usuario", tags=["EstadoUsuario"])


@router.get("/", response_model=list[EstadoUsuarioPublic])
def listar(db: Session = Depends(get_db)):
    return EstadoUsuarioService.get_all(db)


@router.get("/{estado_id}", response_model=EstadoUsuarioPublic)
def obtener(estado_id: int, db: Session = Depends(get_db)):
    estado = EstadoUsuarioService.get(db, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="EstadoUsuario no encontrado")
    return estado


@router.post("/", response_model=EstadoUsuarioPublic)
def crear(data: EstadoUsuarioCreate, db: Session = Depends(get_db)):
    return EstadoUsuarioService.create(db, data)


@router.put("/{estado_id}", response_model=EstadoUsuarioPublic)
def actualizar(estado_id: int, data: EstadoUsuarioUpdate, db: Session = Depends(get_db)):
    estado = EstadoUsuarioService.get(db, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="EstadoUsuario no encontrado")
    return EstadoUsuarioService.update(db, estado, data)


@router.delete("/{estado_id}", response_model=EstadoUsuarioPublic)
def eliminar(estado_id: int, db: Session = Depends(get_db)):
    estado = EstadoUsuarioService.get(db, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="EstadoUsuario no encontrado")
    return EstadoUsuarioService.soft_delete(db, estado)
