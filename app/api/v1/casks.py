from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.cask import Cask
from app.models.user import User
from app.schemas.cask import CaskOut

router = APIRouter()


@router.get("", response_model=list[CaskOut])
def list_casks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        return db.query(Cask).all()
    return db.query(Cask).filter(Cask.owner_id == current_user.id).all()


@router.get("/{cask_id}", response_model=CaskOut)
def get_cask(
    cask_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Cask).filter(Cask.id == cask_id)
    if current_user.role != "admin":
        query = query.filter(Cask.owner_id == current_user.id)

    cask = query.first()
    if not cask:
        raise HTTPException(status_code=404, detail="Cask not found")

    return cask
