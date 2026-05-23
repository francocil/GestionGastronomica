from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tenant import TenantCreate, TenantResponse, TenantBase
from app.services import tenant_service

from app.core.permissions import require_any_admin

router = APIRouter(
    prefix="/admin/tenants",
    tags=["Admin - Tenants"],
)


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(
    tenant_in: TenantCreate,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    if tenant_in.cuit:
        existing = tenant_service.get_tenant_by_cuit(db, tenant_in.cuit)
        if existing:
            raise HTTPException(400, "Ya existe un tenant con ese CUIT.")
    return tenant_service.create_tenant(db, tenant_in)


@router.get("", response_model=List[TenantResponse])
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    only_active: bool = True,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    return tenant_service.list_tenants(db, skip, limit, only_active)


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    tenant = tenant_service.get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(404, "Tenant no encontrado.")
    return tenant


@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    tenant_in: TenantBase,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    tenant = tenant_service.update_tenant(db, tenant_id, tenant_in)
    if not tenant:
        raise HTTPException(404, "Tenant no encontrado.")
    return tenant


@router.delete("/{tenant_id}", response_model=TenantResponse)
def deactivate_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    tenant = tenant_service.deactivate_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(404, "Tenant no encontrado.")
    return tenant
