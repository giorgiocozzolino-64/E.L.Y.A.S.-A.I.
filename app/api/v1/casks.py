from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.cask import Cask
from app.schemas.cask import CaskOut
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/casks", response_model=List[CaskOut])
def list_casks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Cask).filter(Cask.owner_id == current_user.id).all()