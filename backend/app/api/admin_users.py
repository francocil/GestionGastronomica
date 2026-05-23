from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserBase, UserUpdate

from app.services import user_service
from app.core.permissions import require_any_admin

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - Users"],
)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    existing = user_service.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email",
        )

    return user_service.create_user(db, user_in)


@router.get("", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    only_active: bool = True,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    return user_service.list_users(db, skip, limit, only_active)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    user_obj = user_service.get_user(db, user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user_obj


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    user_obj = user_service.update_user(db, user_id, user_in)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user_obj


@router.delete("/{user_id}", response_model=UserResponse)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_any_admin),
):
    user_obj = user_service.deactivate_user(db, user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user_obj
