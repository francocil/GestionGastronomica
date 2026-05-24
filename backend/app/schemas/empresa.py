from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class EmpresaBase(BaseModel):
    cuit_cuil: str
    razon_social: str
    nombre_fantasia: Optional[str] = None
    direccion_fiscal: Optional[str] = None
    email_contacto: Optional[EmailStr] = None
    telefono_contacto: Optional[str] = None
    activo: Optional[bool] = True
    configuracion_fiscal_id: Optional[int] = None
    configuracion_delivery_id: Optional[int] = None
    logo_url: Optional[str] = None
    timezone: Optional[str] = None
    moneda_id: Optional[int] = None
    condicion_iva: Optional[str] = None
    ingresos_brutos: Optional[str] = None
    plan_suscripcion_id: Optional[int] = None


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    razon_social: Optional[str] = None
    nombre_fantasia: Optional[str] = None
    direccion_fiscal: Optional[str] = None
    email_contacto: Optional[EmailStr] = None
    telefono_contacto: Optional[str] = None
    activo: Optional[bool] = None
    configuracion_fiscal_id: Optional[int] = None
    configuracion_delivery_id: Optional[int] = None
    logo_url: Optional[str] = None
    timezone: Optional[str] = None
    moneda_id: Optional[int] = None
    condicion_iva: Optional[str] = None
    ingresos_brutos: Optional[str] = None
    plan_suscripcion_id: Optional[int] = None
    eliminado: Optional[bool] = None


class EmpresaInDB(EmpresaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    eliminado: bool

    class Config:
        from_attributes = True


class EmpresaPublic(EmpresaInDB):
    pass
