from __future__ import annotations

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.receta import Receta
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)


# ============================================================
# HELPERS
# ============================================================

def _calcular_costo_desde_receta(
    db: Session,
    producto_id: int,
    tenant_id: int,
) -> Optional[float]:
    receta = (
        db.query(Receta)
        .filter(
            Receta.producto_id == producto_id,
            Receta.tenant_id == tenant_id,
        )
        .first()
    )

    if not receta:
        return None

    total = 0.0
    for detalle in receta.detalles:
        total += detalle.costo_parcial

    return total


# ============================================================
# CREATE
# ============================================================

def create_product(
    db: Session,
    tenant_id: int,
    data: ProductCreate,
) -> ProductResponse:

    producto = Product(
        tenant_id=tenant_id,
        nombre=data.nombre,
        descripcion=data.descripcion,
        sku=data.sku,
        precio=data.precio,
        costo=data.costo,
        imagen_url=data.imagen_url,
        categoria_id=data.categoria_id,
        unidad_medida_id=data.unidad_medida_id,
        sucursal_id=data.sucursal_id,
    )

    db.add(producto)
    db.commit()
    db.refresh(producto)

    # Si tiene receta → recalcular costo
    costo_receta = _calcular_costo_desde_receta(
        db=db,
        producto_id=producto.id,
        tenant_id=tenant_id,
    )
    if costo_receta is not None:
        producto.costo = costo_receta
        db.commit()
        db.refresh(producto)

    return ProductResponse.from_orm(producto)


# ============================================================
# UPDATE
# ============================================================

def update_product(
    db: Session,
    product_id: int,
    tenant_id: int,
    data: ProductUpdate,
) -> Optional[ProductResponse]:

    producto = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.tenant_id == tenant_id,
            Product.deleted_at.is_(None),
        )
        .first()
    )

    if not producto:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(producto, field, value)

    # Si tiene receta → recalcular costo
    costo_receta = _calcular_costo_desde_receta(
        db=db,
        producto_id=producto.id,
        tenant_id=tenant_id,
    )
    if costo_receta is not None:
        producto.costo = costo_receta

    db.commit()
    db.refresh(producto)

    return ProductResponse.from_orm(producto)


# ============================================================
# LIST SIMPLE
# ============================================================

def list_products(
    db: Session,
    tenant_id: int,
    categoria_id: Optional[int] = None,
    sucursal_id: Optional[int] = None,
    activos: Optional[bool] = None,
) -> list[ProductResponse]:

    q = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id,
            Product.deleted_at.is_(None),
        )
        .order_by(Product.nombre.asc())
    )

    if categoria_id is not None:
        q = q.filter(Product.categoria_id == categoria_id)

    if sucursal_id is not None:
        q = q.filter(Product.sucursal_id == sucursal_id)

    if activos is not None:
        q = q.filter(Product.activo == activos)

    productos = q.all()

    return [ProductResponse.from_orm(p) for p in productos]


# ============================================================
# LIST ADVANCED (USADO POR TU ROUTER)
# ============================================================

def list_products_advanced(
    db: Session,
    tenant_id: int,
    page: int,
    limit: int,
    search: Optional[str],
    activo: Optional[bool],
    min_precio: Optional[float],
    max_precio: Optional[float],
    sort_by: Optional[str],
    order: Optional[str],
    fecha_desde: Optional[str],
    fecha_hasta: Optional[str],
    fecha_actualizacion_desde: Optional[str],
    fecha_actualizacion_hasta: Optional[str],
) -> Dict[str, Any]:

    q = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id,
            Product.deleted_at.is_(None),
        )
    )

    if search:
        q = q.filter(Product.nombre.ilike(f"%{search}%"))

    if activo is not None:
        q = q.filter(Product.activo == activo)

    if min_precio is not None:
        q = q.filter(Product.precio >= min_precio)

    if max_precio is not None:
        q = q.filter(Product.precio <= max_precio)

    # Ordenamiento
    if sort_by:
        col = getattr(Product, sort_by, None)
        if col is not None:
            if order == "desc":
                q = q.order_by(col.desc())
            else:
                q = q.order_by(col.asc())

    total = q.count()

    items = (
        q.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "items": [ProductResponse.from_orm(p) for p in items],
    }


# ============================================================
# GET BY ID
# ============================================================

def get_product(
    db: Session,
    product_id: int,
    tenant_id: int,
) -> Optional[ProductResponse]:

    producto = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.tenant_id == tenant_id,
            Product.deleted_at.is_(None),
        )
        .first()
    )

    if not producto:
        return None

    return ProductResponse.from_orm(producto)


# ============================================================
# DELETE (SOFT DELETE)
# ============================================================

def deactivate_product(
    db: Session,
    product_id: int,
    tenant_id: int,
) -> Optional[ProductResponse]:

    producto = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.tenant_id == tenant_id,
            Product.deleted_at.is_(None),
        )
        .first()
    )

    if not producto:
        return None

    producto.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(producto)

    return ProductResponse.from_orm(producto)
