# ==================================================================================================
# Sistema de Permisos (PBAC Nivel Base)
# Este archivo define dependencias globales para validar:
# - Autenticación
# - Permisos por rol
#
# IMPORTANTE:
# - Este archivo reemplaza el sistema basado en nombres de rol.
# - No rompe IAM Avanzado.
# - No depende del middleware JWT, solo lo complementa.
# ==================================================================================================

from typing import cast, List
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.request_state import AuthenticatedState
from app.db.session import get_db
from app.services.role_service import get_role_with_permissions


# ============================================================================================
# 1) Verificar usuario autenticado
# ============================================================================================
def require_authenticated_user(request: Request):
    """
    Verifica que el usuario esté autenticado.
    El middleware JWT ya validó el token y cargó request.state.auth.
    """
    if not hasattr(request.state, "auth"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
        )

    auth = cast(AuthenticatedState, request.state.auth)

    if not auth.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
        )

    return auth


# ============================================================================================
# 2) Obtener permisos del rol actual
# ============================================================================================
def get_current_permissions(
    auth: AuthenticatedState = Depends(require_authenticated_user),
    db: Session = Depends(get_db)
) -> List[str]:
    """
    Devuelve la lista de permisos del rol actual del usuario.
    """

    if auth.role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario debe seleccionar un tenant antes de continuar"
        )

    role = get_role_with_permissions(db, auth.role)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no encontrado o sin permisos"
        )

    return [p.nombre for p in role.permissions]


# ============================================================================================
# 3) Validar un permiso específico
# ============================================================================================
def require_permission(permission_name: str):

    def dependency(
        permissions: List[str] = Depends(get_current_permissions)
    ):
        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: {permission_name}"
            )
        return True

    return dependency


# ============================================================================================
# 4) Validar que tenga AL MENOS UNO de varios permisos
# ============================================================================================
def require_any_permission(required: List[str]):

    def dependency(
        permissions: List[str] = Depends(get_current_permissions)
    ):
        if not any(p in permissions for p in required):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere al menos uno de estos permisos: {required}"
            )
        return True

    return dependency


# ============================================================================================
# 5) Validar que tenga TODOS los permisos indicados
# ============================================================================================
def require_all_permissions(required: List[str]):

    def dependency(
        permissions: List[str] = Depends(get_current_permissions)
    ):
        if not all(p in permissions for p in required):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requieren TODOS estos permisos: {required}"
            )
        return True

    return dependency


# ============================================================================================
# 6) NUEVO — Validar que sea un ADMIN (cualquier tipo de admin)
# ============================================================================================
def require_any_admin():
    """
    Un admin es cualquier usuario que tenga al menos uno de los permisos administrativos.
    """
    admin_permissions = [
        "can_manage_tenants",
        "can_manage_users",
        "can_manage_roles",
        "can_manage_permissions",
    ]

    return require_any_permission(admin_permissions)
