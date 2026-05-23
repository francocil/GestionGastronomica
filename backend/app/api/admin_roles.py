from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut, RoleBase
from app.services.role_service import (
    create_role,
    get_role,
    list_roles,
    update_role,
    deactivate_role,
)

router = APIRouter(prefix="/admin/roles", tags=["Admin - Roles"])


@router.get("/", response_model=list[RoleBase])
def listar_roles(db: Session = Depends(get_db)):
    return list_roles(db)


@router.get("/{role_id}", response_model=RoleOut)
def obtener_role(role_id: int, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role


@router.post("/", response_model=RoleOut)
def crear_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role_in)


@router.put("/{role_id}", response_model=RoleOut)
def actualizar_role(role_id: int, role_in: RoleUpdate, db: Session = Depends(get_db)):
    role = update_role(db, role_id, role_in)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role


@router.delete("/{role_id}", response_model=RoleBase)
def desactivar_role(role_id: int, db: Session = Depends(get_db)):
    role = deactivate_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role
