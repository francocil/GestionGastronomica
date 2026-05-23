from fastapi import FastAPI
from app.api.router import router as api_router
from app.core.security import AuthMiddleware

app = FastAPI(
    title="Plataforma Integral de Gestión Gastronómica",
    version="0.1.0",
    description="Backend base inicial (Fase 0)"
)

# Registrar middleware
app.add_middleware(AuthMiddleware)

# Montar router
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend operativo - Fase 0"}
