from pydantic import BaseModel
from typing import List, Optional

# ============================================================
# PERMISSION BASE
# ============================================================
class PermissionBase(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True


# ============================================================
# ROLE BASE (para lectura)
# ============================================================
class RoleBase(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool

    class Config:
        orm_mode = True


# ============================================================
# ROLE CREATE (para creación)
# ============================================================
class RoleCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
# ROLE UPDATE (opcional, pero recomendado)
# ============================================================
class RoleUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
# ROLE OUT (CON PERMISOS)
# ============================================================
class RoleOut(RoleBase):
    permissions: List[PermissionBase]
