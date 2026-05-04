from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.listing import Listing
from app.schemas.listing import ListingOut

router = APIRouter()


@router.get("/casks", response_model=list[ListingOut])
def cask_exchange(db: Session = Depends(get_db)):
    return db.query(Listing).filter(
        Listing.asset_type == "cask",
        Listing.market == "exchange",
        Listing.status == "active",
    ).all()


@router.get("/bottles", response_model=list[ListingOut])
def bottle_exchange(db: Session = Depends(get_db)):
    return db.query(Listing).filter(
        Listing.asset_type == "bottle",
        Listing.market == "exchange",
        Listing.status == "active",
    ).all()
