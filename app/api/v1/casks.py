from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os

from app.db.session import get_db
from app.models.cask import Cask
from app.schemas.cask import CaskOut

router = APIRouter()

security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_SUPER_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


@router.get("/", response_model=List[CaskOut])
def list_casks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_payload),
):
    role = current_user.get("role")
    user_id = int(current_user.get("sub"))

    if role == "admin":
        return db.query(Cask).all()

    if role == "broker":
        return db.query(Cask).filter(Cask.status == "maturing").all()

    return db.query(Cask).filter(Cask.owner_id == user_id).all()