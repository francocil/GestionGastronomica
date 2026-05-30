from fastapi import APIRouter

# Routers existentes
from app.api.auth import router as auth_router
from app.api.admin_users import router as admin_users_router
from app.api.admin_roles import router as admin_roles_router
from app.api.admin_tenants import router as admin_tenants_router
from app.api.admin_empresas import router as admin_empresas_router
from app.api.admin_assignments import router as admin_assignments_router
from app.api.categorias import router as categorias_router
from app.api.products import router as products_router
from app.api.tipo_usuario import router as tipo_usuario_router
from app.api.estado_usuario import router as estado_usuario_router
from app.api.mfa_estado import router as mfa_estado_router

# Routers gastronómicos nuevos
from app.api.unidades_medida import router as unidades_medida_router
from app.api.insumos import router as insumos_router
from app.api.sucursales import router as sucursales_router
from app.api.stock_movimientos import router as stock_movimientos_router
from app.api.recetas import router as recetas_router
from app.api.receta_detalle import router as receta_detalle_router


api_router = APIRouter()

# Registro de routers existentes
api_router.include_router(auth_router)
api_router.include_router(admin_users_router)
api_router.include_router(admin_roles_router)
api_router.include_router(admin_tenants_router)
api_router.include_router(admin_empresas_router)
api_router.include_router(admin_assignments_router)
api_router.include_router(categorias_router)
api_router.include_router(products_router)
api_router.include_router(tipo_usuario_router)
api_router.include_router(estado_usuario_router)
api_router.include_router(mfa_estado_router)

# Registro de routers gastronómicos
api_router.include_router(unidades_medida_router)
api_router.include_router(insumos_router)
api_router.include_router(sucursales_router)
api_router.include_router(stock_movimientos_router)
api_router.include_router(recetas_router)
api_router.include_router(receta_detalle_router)
