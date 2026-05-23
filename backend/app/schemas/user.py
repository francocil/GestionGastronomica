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


# ---------------------------------------------------------
# Base común para creación y actualización
# ---------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
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
    nombre: str | None = None
    apellido: str | None = None
    activo: bool | None = None


# ---------------------------------------------------------
# Respuesta pública del usuario
# ---------------------------------------------------------
class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# Usuario con rol y tenant (para IAM)
# ---------------------------------------------------------
class UserWithTenantRole(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    apellido: str
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
