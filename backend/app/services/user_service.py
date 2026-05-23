from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import hash_password


# ============================================================
# CREATE USER
# ============================================================
def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        nombre=user_in.nombre,
        apellido=user_in.apellido,
        activo=user_in.activo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ============================================================
# GET USER BY ID
# ============================================================
def get_user(db: Session, user_id: int) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


# ============================================================
# GET USER BY EMAIL
# ============================================================
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)


# ============================================================
# LIST USERS
# ============================================================
def list_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = True,
) -> List[User]:
    stmt = select(User)

    if only_active:
        stmt = stmt.where(User.activo == True)  # noqa: E712

    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt))


# ============================================================
# UPDATE USER
# ============================================================
def update_user(
    db: Session,
    user_id: int,
    user_in: UserUpdate,
) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None

    # Campos opcionales (UserUpdate)
    if user_in.nombre is not None:
        user.nombre = user_in.nombre

    if user_in.apellido is not None:
        user.apellido = user_in.apellido

    if user_in.activo is not None:
        user.activo = user_in.activo

    db.commit()
    db.refresh(user)
    return user


# ============================================================
# DEACTIVATE USER (SOFT DELETE)
# ============================================================
def deactivate_user(db: Session, user_id: int) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None

    user.activo = False
    db.commit()
    db.refresh(user)
    return user
