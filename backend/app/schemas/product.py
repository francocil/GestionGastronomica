# ==========================================================================================
# Schemas de Producto
#
# Estos schemas definen las estructuras de entrada y salida utilizadas para:
# - Crear productos
# - Actualizar productos
# - Listar productos
# - Representar productos dentro del sistema multi‑tenant
#
# Compatibles con Pydantic v2 y con los modelos ORM.
# ==========================================================================================

from pydantic import BaseModel


# ---------------------------------------------------------
# Base común para creación y actualización
# ---------------------------------------------------------
class ProductBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    activo: bool = True


# ---------------------------------------------------------
# Crear producto
# ---------------------------------------------------------
class ProductCreate(ProductBase):
    tenant_id: int


# ---------------------------------------------------------
# Actualizar producto
# ---------------------------------------------------------
class ProductUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    activo: bool | None = None


# ---------------------------------------------------------
# Respuesta pública del producto
# ---------------------------------------------------------
class ProductResponse(ProductBase):
    id: int
    tenant_id: int

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# Listado de productos (útil para endpoints paginados)
# ---------------------------------------------------------
class ProductListResponse(BaseModel):
    total: int
    items: list[ProductResponse]
