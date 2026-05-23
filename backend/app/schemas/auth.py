# ===============================================================================
# Estos schemas definen las estructuras de entrada y salida utilizadas en el
# proceso de autenticación del sistema IAM. Su propósito es:
#
# - Validar credenciales de acceso (email y contraseña).
# - Estandarizar la respuesta del login con tokens JWT.
# - Representar al usuario autenticado dentro del contexto de un tenant.
# - Mantener compatibilidad con Pydantic v2.
# - Servir como base para los endpoints /auth/login y /auth/refresh.
# ===============================================================================

from pydantic import BaseModel, EmailStr
from typing import Optional

from app.schemas.role import RoleOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthenticatedUser(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    apellido: str
    tenant_id: int
    role: RoleOut   # ← AHORA ACEPTA EL ROL COMPLETO
