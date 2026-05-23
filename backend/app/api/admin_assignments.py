from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import user_tenant_role_service

from app.core.permissions import require_any_admin

router = APIRouter(
    prefix="/admin/assignments",
    tags=["Admin - Assignments"],
)


@router.post("", response_model=dict)
def assign_role(
    user_id: int,
    tenant_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    utr = user_tenant_role_service.assign_role(db, user_id, tenant_id, role_id)
    return {"id": utr.id, "detail": "Asignación creada"}


@router.get("", response_model=List[dict])
def list_assignments(
    user_id: int | None = None,
    tenant_id: int | None = None,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    assignments = user_tenant_role_service.list_assignments(db, user_id, tenant_id)
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "tenant_id": a.tenant_id,
            "role_id": a.role_id,
        }
        for a in assignments
    ]


@router.delete("/{assignment_id}", response_model=dict)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_any_admin)
):
    ok = user_tenant_role_service.delete_assignment(db, assignment_id)
    if not ok:
        raise HTTPException(404, "Asignación no encontrada")
    return {"detail": "Asignación eliminada"}
