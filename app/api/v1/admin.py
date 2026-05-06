from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.cask import Cask
from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        return []

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
        }
        for u in users
    ]


@router.get("/casks")
def get_casks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        return []

    casks = db.query(Cask).all()

    return [
        {
            "id": c.id,
            "cask_code": c.cask_code,
            "distillery": c.distillery,
            "owner_id": c.owner_id,
            "current_value_gbp": c.current_value_gbp,
            "projected_value_gbp": c.projected_value_gbp,
        }
        for c in casks
    ]