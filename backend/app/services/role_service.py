from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


def create_role(db: Session, role_in: RoleCreate) -> Role:
    role = Role(
        nombre=role_in.nombre,
        descripcion=role_in.descripcion,
        activo=role_in.activo,
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role(db: Session, role_id: int) -> Optional[Role]:
    stmt = select(Role).where(Role.id == role_id)
    return db.scalar(stmt)


def get_role_by_nombre(db: Session, nombre: str) -> Optional[Role]:
    stmt = select(Role).where(Role.nombre == nombre)
    return db.scalar(stmt)


def list_roles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = True,
) -> List[Role]:
    stmt = select(Role)
    if only_active:
        stmt = stmt.where(Role.activo == True)  # noqa: E712
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt))


def update_role(
    db: Session,
    role_id: int,
    role_in: RoleUpdate,
) -> Optional[Role]:
    role = get_role(db, role_id)
    if not role:
        return None

    role.nombre = role_in.nombre
    role.descripcion = role_in.descripcion
    role.activo = role_in.activo

    db.commit()
    db.refresh(role)
    return role


def deactivate_role(db: Session, role_id: int) -> Optional[Role]:
    role = get_role(db, role_id)
    if not role:
        return None

    role.activo = False
    db.commit()
    db.refresh(role)
    return role


# ============================================================
# NUEVO: obtener rol + permisos (para /auth/me y middleware)
# ============================================================
def get_role_with_permissions(db: Session, role_name: str) -> Optional[Role]:
    """
    Devuelve el rol con sus permisos cargados.
    """
    stmt = select(Role).where(Role.nombre == role_name)
    role = db.scalar(stmt)

    return role
