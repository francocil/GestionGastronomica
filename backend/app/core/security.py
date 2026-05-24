# ===============================================================================
# Middleware de Autenticación (JWT)
# Este middleware:
# - Lee el token JWT desde el header Authorization: Bearer <token>.
# - Valida el token y extrae el usuario autenticado.
# - Inyecta user_id, tenant_id y role en request.state.
# - Permite que los endpoints accedan al usuario autenticado sin repetir lógica.
# ===============================================================================

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError

from app.services.auth_service import decode_token
from app.core.request_state import AuthenticatedState


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # ============================================================
        # 1) PERMITIR PRE-FLIGHT OPTIONS (CORS)
        # ============================================================
        if request.method == "OPTIONS":
            return await call_next(request)

        # ============================================================
        # 2) RUTAS PÚBLICAS (sin autenticación)
        # ============================================================
        public_paths = [
            "/auth/login",
            "/api/auth/login",
            "/auth/select-tenant",
            "/api/auth/select-tenant",
            "/api/status",
            "/docs",
            "/openapi.json",
        ]

        if request.url.path in public_paths:
            return await call_next(request)

        # ============================================================
        # 3) LEER TOKEN JWT
        # ============================================================
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token no proporcionado"}
            )

        token = auth_header.split(" ")[1]

        # ============================================================
        # 4) VALIDAR TOKEN
        # ============================================================
        try:
            payload = decode_token(token)
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token inválido o expirado"}
            )

        if not payload:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token inválido o expirado"}
            )

        # ============================================================
        # 5) INYECTAR USUARIO AUTENTICADO
        # ============================================================
        state = AuthenticatedState()
        state.user_id = int(payload["sub"])
        state.tenant_id = payload.get("tenant_id")
        state.role = payload.get("role")

        request.state.auth = state

        return await call_next(request)
