# ==========================================================================
# Schemas de Usuario (IAM)
#
# Estos schemas definen las estructuras de entrada y salida utilizadas para:
# - Crear usuarios
# - Actualizar usuarios
# - Listar usuarios
# - Representar usuarios con roles y tenants
#
# Compatibles con Pydantic v2 y con los modelos ORM.
# ==========================================================================

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------
# Base común para creación y actualización
# (Alineado 1:1 al SRS)
# ---------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str
    telefono: Optional[str] = None
    empresa_id: Optional[int] = None
    tipo_usuario_id: int
    estado_usuario_id: int
    mfa_estado_id: int
    activo: bool = True


# ---------------------------------------------------------
# Crear usuario (incluye password)
# ---------------------------------------------------------
class UserCreate(UserBase):
    password: str


# ---------------------------------------------------------
# Actualizar usuario (sin password)
# ---------------------------------------------------------
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    estado_usuario_id: Optional[int] = None
    mfa_estado_id: Optional[int] = None
    activo: Optional[bool] = None


# ---------------------------------------------------------
# Respuesta pública del usuario
# ---------------------------------------------------------
class UserResponse(UserBase):
    id: int
    fecha_creacion: datetime
    fecha_ultimo_login: Optional[datetime] = None
    eliminado: bool

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# Usuario con rol y tenant (para IAM)
# ---------------------------------------------------------
class UserWithTenantRole(BaseModel):
    id: int
    email: EmailStr
    username: str
    tenant_id: int
    role: str

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# Listado de usuarios (útil para endpoints paginados)
# ---------------------------------------------------------
class UserListResponse(BaseModel):
    total: int
    items: list[UserResponse]
