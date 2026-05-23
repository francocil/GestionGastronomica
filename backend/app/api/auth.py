# =========================================================================
# Endpoints de Autenticación (versión definitiva para Web + Móvil)
# =========================================================================
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, AuthenticatedUser
from app.schemas.role import RoleOut
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_user_tenant_role,
    decode_token
)
from app.services.role_service import get_role_with_permissions
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================================================================
# /auth/login  →  Cookies HttpOnly (Web) + Token JSON (Móvil)
# =========================================================================
@router.post("/login")
def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Construimos lista de tenants del usuario
    tenants = [
        {
            "tenant_id": utr.tenant_id,
            "tenant_nombre": utr.tenant.nombre,
            "role": utr.role.nombre
        }
        for utr in user.tenants
    ]

    # Si tiene un solo tenant → seleccionarlo automáticamente
    if len(tenants) == 1:
        tenant_id = tenants[0]["tenant_id"]
        role = tenants[0]["role"]
        requires_tenant_selection = False
    else:
        tenant_id = None
        role = None
        requires_tenant_selection = True

    # Crear token
    token = create_access_token({
        "sub": str(user.id),
        "tenant_id": tenant_id,
        "role": role
    })

    # Detectar tipo de cliente
    client_type = request.headers.get("X-Client-Type", "web")

    # ============================================================
    # WEB → Cookie HttpOnly
    # ============================================================
    if client_type == "web":
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=60 * 15  # 15 minutos
        )

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "nombre": user.nombre,
                "apellido": user.apellido,
            },
            "tenants": tenants,
            "requires_tenant_selection": requires_tenant_selection
        }

    # ============================================================
    # MÓVIL → Token en JSON
    # ============================================================
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
        },
        "tenants": tenants,
        "requires_tenant_selection": requires_tenant_selection
    }


# =========================================================================
# /auth/me  →  Devuelve usuario + tenant + rol + permisos
# =========================================================================
@router.get("/me", response_model=AuthenticatedUser)
def get_me(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    user_id = int(payload["sub"])
    tenant_id = payload.get("tenant_id")
    role_name = payload.get("role")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    if tenant_id is None:
        raise HTTPException(
            status_code=400,
            detail="El usuario debe seleccionar un tenant"
        )

    utr = get_user_tenant_role(db, user_id, tenant_id)

    if not utr:
        raise HTTPException(
            status_code=403,
            detail="El usuario no pertenece a este tenant"
        )

    # ============================================================
    # Validación adicional para evitar error de Pylance
    # ============================================================
    if role_name is None:
        raise HTTPException(
            status_code=400,
            detail="El usuario debe seleccionar un tenant antes de consultar /auth/me"
        )

    # Obtener rol + permisos
    role = get_role_with_permissions(db, role_name)

    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Rol '{role_name}' no encontrado"
        )

    return AuthenticatedUser(
        id=user.id,
        email=user.email,
        nombre=user.nombre,
        apellido=user.apellido,
        tenant_id=tenant_id,
        role=RoleOut(
            id=role.id,
            nombre=role.nombre,
            descripcion=role.descripcion,
            activo=role.activo,
            permissions=role.permissions
        )
    )


# =========================================================================
# /auth/select-tenant
# =========================================================================
@router.post("/select-tenant")
def select_tenant(token: str, tenant_id: int, db: Session = Depends(get_db)):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    user_id = int(payload["sub"])

    utr = get_user_tenant_role(db, user_id, tenant_id)

    if not utr:
        raise HTTPException(
            status_code=403,
            detail="El usuario no pertenece a este tenant"
        )

    new_token = create_access_token({
        "sub": str(user_id),
        "tenant_id": tenant_id,
        "role": utr.role.nombre
    })

    return {
        "access_token": new_token,
        "tenant_id": tenant_id,
        "role": utr.role.nombre
    }
