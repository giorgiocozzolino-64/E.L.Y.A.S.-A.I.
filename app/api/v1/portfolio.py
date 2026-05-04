from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.cask import Cask
from app.models.user import User
from app.schemas.cask import PortfolioSummary

router = APIRouter()


@router.get("/summary", response_model=PortfolioSummary)
def portfolio_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Cask)
    if current_user.role != "admin":
        query = query.filter(Cask.owner_id == current_user.id)

    casks = query.all()

    total_value = sum(c.current_value_gbp for c in casks)
    total_projected = sum(c.projected_value_gbp for c in casks)
    purchase_total = sum(c.purchase_price_gbp for c in casks) or 1
    avg_score = sum(c.maturation_score for c in casks) / len(casks) if casks else 0
    roi = ((total_value - purchase_total) / purchase_total) * 100

    return PortfolioSummary(
        total_value_gbp=round(total_value, 2),
        total_projected_value_gbp=round(total_projected, 2),
        number_of_casks=len(casks),
        average_maturation_score=round(avg_score, 2),
        average_roi_pct=round(roi, 2),
    )
