from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.services import product_service
from app.core.permissions import require_any_admin

router = APIRouter(
    prefix="/tenant/products",
    tags=["Tenant - Products"],
)


# ============================================================
# CREATE PRODUCT
# ============================================================
@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    tenant_id = request.state.tenant_id

    if product_in.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tenant_id no coincide con el tenant seleccionado.",
        )

    return product_service.create_product(db, product_in)


# ============================================================
# LIST PRODUCTS (ADVANCED)
# ============================================================
@router.get("", response_model=List[ProductResponse])
def list_products(
    request: Request,
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    activo: Optional[bool] = None,
    min_precio: Optional[float] = None,
    max_precio: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    fecha_actualizacion_desde: Optional[str] = None,
    fecha_actualizacion_hasta: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    tenant_id = request.state.tenant_id

    result = product_service.list_products_advanced(
        db=db,
        tenant_id=tenant_id,
        page=page,
        limit=limit,
        search=search,
        activo=activo,
        min_precio=min_precio,
        max_precio=max_precio,
        sort_by=sort_by,
        order=order,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        fecha_actualizacion_desde=fecha_actualizacion_desde,
        fecha_actualizacion_hasta=fecha_actualizacion_hasta,
    )

    return result["items"]


# ============================================================
# GET PRODUCT BY ID
# ============================================================
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    tenant_id = request.state.tenant_id
    product = product_service.get_product(db, product_id, tenant_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    return product


# ============================================================
# UPDATE PRODUCT
# ============================================================
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    tenant_id = request.state.tenant_id
    product = product_service.update_product(db, product_id, tenant_id, product_in)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    return product


# ============================================================
# DELETE PRODUCT (SOFT DELETE)
# ============================================================
@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    tenant_id = request.state.tenant_id
    product = product_service.deactivate_product(db, product_id, tenant_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    return product
