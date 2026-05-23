from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user_tenant_role import UserTenantRole
from app.schemas.user import UserWithTenantRole


def assign_role(db: Session, user_id: int, tenant_id: int, role_id: int) -> UserTenantRole:
    utr = UserTenantRole(
        user_id=user_id,
        tenant_id=tenant_id,
        role_id=role_id,
    )
    db.add(utr)
    db.commit()
    db.refresh(utr)
    return utr

def get_assignment(db: Session, assignment_id: int) -> Optional[UserTenantRole]:
    stmt = select(UserTenantRole).where(UserTenantRole.id == assignment_id)
    return db.scalar(stmt)

def list_assignments(
    db: Session,
    user_id: Optional[int] = None,
    tenant_id: Optional[int] = None,
) -> List[UserTenantRole]:
    stmt = select(UserTenantRole)

    if user_id:
        stmt = stmt.where(UserTenantRole.user_id == user_id)

    if tenant_id:
        stmt = stmt.where(UserTenantRole.tenant_id == tenant_id)

    return list(db.scalars(stmt))

def delete_assignment(db: Session, assignment_id: int) -> bool:
    utr = get_assignment(db, assignment_id)
    if not utr:
        return False

    db.delete(utr)
    db.commit()
    return True
