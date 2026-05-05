from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.cask import Cask
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/portfolio/summary")
def portfolio_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    casks = db.query(Cask).filter(Cask.owner_id == current_user.id).all()

    total_current = sum(c.current_value_gbp for c in casks)
    total_projected = sum(c.projected_value_gbp for c in casks)

    roi = 0
    if total_current > 0:
        roi = ((total_projected - total_current) / total_current) * 100

    avg_maturation = 0
    if casks:
        avg_maturation = sum(c.maturation_score for c in casks) / len(casks)

    return {
        "casks": len(casks),
        "current_value": total_current,
        "projected_value": total_projected,
        "roi": round(roi, 1),
        "avg_maturation": round(avg_maturation, 1)
    }