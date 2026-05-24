from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.stock_movimiento import (
    StockMovimientoCreate,
    StockMovimientoUpdate,
    StockMovimientoPublic,
)
from app.services.stock_movimiento_service import StockMovimientoService

router = APIRouter(prefix="/stock-movimientos", tags=["StockMovimientos"])


@router.get("/", response_model=list[StockMovimientoPublic])
def listar(db: Session = Depends(get_db)):
    return StockMovimientoService.get_all(db)


@router.get("/{mov_id}", response_model=StockMovimientoPublic)
def obtener(mov_id: int, db: Session = Depends(get_db)):
    mov = StockMovimientoService.get(db, mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return mov


@router.post("/", response_model=StockMovimientoPublic)
def crear(data: StockMovimientoCreate, request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    return StockMovimientoService.create(db, data, tenant_id)


@router.put("/{mov_id}", response_model=StockMovimientoPublic)
def actualizar(mov_id: int, data: StockMovimientoUpdate, db: Session = Depends(get_db)):
    mov = StockMovimientoService.get(db, mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return StockMovimientoService.update(db, mov, data)


@router.delete("/{mov_id}", response_model=StockMovimientoPublic)
def eliminar(mov_id: int, db: Session = Depends(get_db)):
    mov = StockMovimientoService.get(db, mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return StockMovimientoService.soft_delete(db, mov)
