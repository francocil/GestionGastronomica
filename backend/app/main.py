from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.core.security import AuthMiddleware

app = FastAPI(
    title="Plataforma Integral de Gestión Gastronómica",
    version="0.1.0",
    description="Backend base inicial (Fase 0)"
)

# ============================
# CONFIGURACIÓN DE CORS
# ============================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,          # Necesario para cookies HttpOnly
    allow_methods=["*"],             # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],             # Authorization, Content-Type, etc.
)

# ============================
# MIDDLEWARE DE AUTENTICACIÓN
# ============================
app.add_middleware(AuthMiddleware)

# ============================
# ROUTER PRINCIPAL
# ============================
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend operativo - Fase 0"}
