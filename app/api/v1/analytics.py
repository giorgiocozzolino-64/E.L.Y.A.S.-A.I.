from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.cask import Cask
from app.models.user import User

router = APIRouter()


@router.get("/portfolio")
def portfolio_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    casks = db.query(Cask).filter(Cask.owner_id == current_user.id).all()

    cask_count = len(casks)

    total_value = sum(float(c.current_value_gbp or 0) for c in casks)
    projected_value = sum(float(c.projected_value_gbp or 0) for c in casks)
    total_invested = sum(float(c.purchase_price_gbp or 0) for c in casks)

    unrealized_gain = total_value - total_invested

    roi = 0
    if total_invested > 0:
        roi = ((total_value - total_invested) / total_invested) * 100

    avg_maturation = 0
    if cask_count > 0:
        avg_maturation = sum(float(c.maturation_score or 0) for c in casks) / cask_count

    avg_risk = 0
    if cask_count > 0:
        avg_risk = sum(float(c.risk_score or 0) for c in casks) / cask_count

    return {
        "cask_count": cask_count,
        "total_value_gbp": round(total_value, 2),
        "projected_value_gbp": round(projected_value, 2),
        "total_invested_gbp": round(total_invested, 2),
        "unrealized_gain_gbp": round(unrealized_gain, 2),
        "roi_pct": round(roi, 2),
        "average_maturation_score": round(avg_maturation, 2),
        "average_risk_score": round(avg_risk, 2),
    }