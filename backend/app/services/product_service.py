from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


# ============================================================
# CREATE PRODUCT
# ============================================================
def create_product(db: Session, product_in: ProductCreate) -> Product:
    product = Product(
        tenant_id=product_in.tenant_id,
        nombre=product_in.nombre,
        descripcion=product_in.descripcion,
        precio=product_in.precio,
        activo=product_in.activo,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# ============================================================
# GET PRODUCT BY ID
# ============================================================
def get_product(db: Session, product_id: int, tenant_id: int) -> Optional[Product]:
    stmt = select(Product).where(
        Product.id == product_id,
        Product.tenant_id == tenant_id
    )
    return db.scalar(stmt)


# ============================================================
# LIST PRODUCTS (PAGINADO + FILTROS + ORDEN + FECHAS)
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
):
    stmt = select(Product).where(Product.tenant_id == tenant_id)

    # Filtro por búsqueda
    if search:
        stmt = stmt.where(Product.nombre.ilike(f"%{search}%"))

    # Filtro activo
    if activo is not None:
        stmt = stmt.where(Product.activo == activo)

    # Filtro por precio
    if min_precio is not None:
        stmt = stmt.where(Product.precio >= min_precio)

    if max_precio is not None:
        stmt = stmt.where(Product.precio <= max_precio)

    # Filtro por fecha de creación
    if fecha_desde:
        stmt = stmt.where(Product.fecha_creacion >= fecha_desde)

    if fecha_hasta:
        stmt = stmt.where(Product.fecha_creacion <= fecha_hasta)

    # Filtro por fecha de actualización
    if fecha_actualizacion_desde:
        stmt = stmt.where(Product.fecha_actualizacion >= fecha_actualizacion_desde)

    if fecha_actualizacion_hasta:
        stmt = stmt.where(Product.fecha_actualizacion <= fecha_actualizacion_hasta)

    # Ordenamiento
    if sort_by in ["nombre", "precio", "activo", "fecha_creacion", "fecha_actualizacion"]:
        column = getattr(Product, sort_by)
        stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

    # Total antes de paginar
    total = db.scalar(
        select(func.count()).select_from(stmt.subquery())
    )

    # Paginación
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)

    items = list(db.scalars(stmt))

    return {
        "total": total,
        "items": items,
    }


# ============================================================
# UPDATE PRODUCT
# ============================================================
def update_product(
    db: Session,
    product_id: int,
    tenant_id: int,
    product_in: ProductUpdate,
) -> Optional[Product]:

    product = get_product(db, product_id, tenant_id)
    if not product:
        return None

    if product_in.nombre is not None:
        product.nombre = product_in.nombre

    if product_in.descripcion is not None:
        product.descripcion = product_in.descripcion

    if product_in.precio is not None:
        product.precio = product_in.precio

    if product_in.activo is not None:
        product.activo = product_in.activo

    db.commit()
    db.refresh(product)
    return product


# ============================================================
# DEACTIVATE PRODUCT (SOFT DELETE)
# ============================================================
def deactivate_product(
    db: Session,
    product_id: int,
    tenant_id: int
) -> Optional[Product]:

    product = get_product(db, product_id, tenant_id)
    if not product:
        return None

    product.activo = False
    db.commit()
    db.refresh(product)
    return product
