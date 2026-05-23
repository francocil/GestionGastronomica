from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantBase


def create_tenant(db: Session, tenant_in: TenantCreate) -> Tenant:
    tenant = Tenant(
        nombre=tenant_in.nombre,
        razon_social=tenant_in.razon_social,
        cuit=tenant_in.cuit,
        activo=tenant_in.activo,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def get_tenant(db: Session, tenant_id: int) -> Optional[Tenant]:
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    return db.scalar(stmt)


def get_tenant_by_cuit(db: Session, cuit: str) -> Optional[Tenant]:
    stmt = select(Tenant).where(Tenant.cuit == cuit)
    return db.scalar(stmt)


def list_tenants(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = True,
) -> List[Tenant]:
    stmt = select(Tenant)
    if only_active:
        stmt = stmt.where(Tenant.activo == True)  # noqa: E712
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt))


def update_tenant(
    db: Session,
    tenant_id: int,
    tenant_in: TenantBase,
) -> Optional[Tenant]:
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return None

    tenant.nombre = tenant_in.nombre
    tenant.razon_social = tenant_in.razon_social
    tenant.cuit = tenant_in.cuit
    tenant.activo = tenant_in.activo

    db.commit()
    db.refresh(tenant)
    return tenant


def deactivate_tenant(db: Session, tenant_id: int) -> Optional[Tenant]:
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return None

    tenant.activo = False
    db.commit()
    db.refresh(tenant)
    return tenant
