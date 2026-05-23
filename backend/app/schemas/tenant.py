# ========================================================================
# Estos schemas definen las estructuras de entrada y salida utilizadas para
# crear, actualizar y devolver información de empresas dentro del sistema
# multi‑tenant.
# Su propósito es:
# - Validar datos de entrada al crear o modificar tenants.
# - Estandarizar la representación pública de un tenant.
# - Integrarse con el modelo Tenant y con UserTenantRole.
# - Mantener compatibilidad con Pydantic v2.
# ========================================================================
from pydantic import BaseModel

class TenantBase(BaseModel):
    nombre: str
    razon_social: str | None = None
    cuit: str | None = None
    activo: bool = True

class TenantCreate(TenantBase):
    pass

class TenantResponse(TenantBase):
    id: int

    class Config:
        from_attributes = True
