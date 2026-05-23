from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api import (
    admin_roles,
    admin_tenants,
    admin_users,
    admin_assignments,
)

router = APIRouter()

# Auth
router.include_router(auth_router)

# IAM Admin
router.include_router(admin_roles.router)
router.include_router(admin_tenants.router)
router.include_router(admin_users.router)
router.include_router(admin_assignments.router)


@router.get("/status")
def status():
    return {"status": "ok"}

# Productos
from app.api import products
router.include_router(products.router)
