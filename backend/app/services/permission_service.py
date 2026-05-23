from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.permission import Permission

def get_all_permissions(db: Session):
    return list(db.scalars(select(Permission)))
