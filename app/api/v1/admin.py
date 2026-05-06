from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.cask import Cask
from app.models.user import User

router = APIRouter()


def require_admin(current_user: User):
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    users = db.query(User).order_by(User.id.asc()).all()

    result = []
    for u in users:
        result.append({
            "id": getattr(u, "id", None),
            "email": getattr(u, "email", ""),
            "full_name": getattr(u, "full_name", ""),
            "role": getattr(u, "role", ""),
            "is_active": getattr(u, "is_active", True),
        })

    return result


@router.get("/casks")
def list_all_casks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    casks = db.query(Cask).order_by(Cask.id.asc()).all()

    result = []
    for c in casks:
        result.append({
            "id": getattr(c, "id", None),
            "cask_code": getattr(c, "cask_code", ""),
            "distillery": getattr(c, "distillery", ""),
            "warehouse": getattr(c, "warehouse", ""),
            "cask_type": getattr(c, "cask_type", ""),
            "owner_id": getattr(c, "owner_id", None),
            "current_value_gbp": getattr(c, "current_value_gbp", 0),
            "projected_value_gbp": getattr(c, "projected_value_gbp", 0),
            "maturation_score": getattr(c, "maturation_score", 0),
            "risk_score": getattr(c, "risk_score", 0),
            "status": getattr(c, "status", ""),
        })

    return result