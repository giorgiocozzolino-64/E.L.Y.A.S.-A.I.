from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.listing import Listing
from app.schemas.listing import ListingOut

router = APIRouter()


@router.get("/offers", response_model=list[ListingOut])
def marketplace_offers(db: Session = Depends(get_db)):
    return db.query(Listing).filter(Listing.status == "active").all()


@router.get("/shop", response_model=list[ListingOut])
def online_shop(db: Session = Depends(get_db)):
    return db.query(Listing).filter(
        Listing.market == "shop",
        Listing.status == "active",
    ).all()
