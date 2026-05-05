from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.security import hash_password
from app.db.session import get_db
from app.models.cask import Cask
from app.models.user import User

router = APIRouter()


class AdminUserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    role: str = "client"


class AdminCaskCreate(BaseModel):
    owner_id: int
    cask_code: str
    distillery: str
    warehouse: str | None = None
    cask_type: str | None = None
    wood_origin: str | None = None
    size_liters: float = 250
    purchase_price_gbp: float = 0
    current_value_gbp: float = 0
    projected_value_gbp: float = 0
    maturation_score: float = 0
    risk_score: float = 0
    abv: float = 0
    fill_level: float = 100
    temperature_c: float = 12.4
    humidity_pct: float = 68
    lbb_device_id: str | None = None
    status: str = "maturing"


def require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    users = db.query(User).order_by(User.id.asc()).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
        }
        for u in users
    ]


@router.post("/users")
def create_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        hashed_password=hash_password(payload.password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
    }


@router.get("/casks")
def list_all_casks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    casks = db.query(Cask).order_by(Cask.id.asc()).all()
    return casks


@router.post("/casks")
def create_cask(
    payload: AdminCaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    owner = db.query(User).filter(User.id == payload.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner user not found")

    existing = db.query(Cask).filter(Cask.cask_code == payload.cask_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cask code already exists")

    cask = Cask(
        owner_id=payload.owner_id,
        cask_code=payload.cask_code,
        distillery=payload.distillery,
        warehouse=payload.warehouse,
        cask_type=payload.cask_type,
        wood_origin=payload.wood_origin,
        size_liters=payload.size_liters,
        purchase_price_gbp=payload.purchase_price_gbp,
        current_value_gbp=payload.current_value_gbp,
        projected_value_gbp=payload.projected_value_gbp,
        maturation_score=payload.maturation_score,
        risk_score=payload.risk_score,
        abv=payload.abv,
        fill_level=payload.fill_level,
        temperature_c=payload.temperature_c,
        humidity_pct=payload.humidity_pct,
        lbb_device_id=payload.lbb_device_id,
        status=payload.status,
    )

    db.add(cask)
    db.commit()
    db.refresh(cask)

    return cask


@router.delete("/casks/{cask_id}")
def delete_cask(
    cask_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    cask = db.query(Cask).filter(Cask.id == cask_id).first()
    if not cask:
        raise HTTPException(status_code=404, detail="Cask not found")

    db.delete(cask)
    db.commit()

    return {"status": "deleted", "cask_id": cask_id}