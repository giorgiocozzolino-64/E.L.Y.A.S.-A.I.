from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.cask import Cask
from app.models.listing import Listing
from app.models.user import User
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


@router.get("/casks")
def marketplace_casks(db: Session = Depends(get_db)):
    listings = db.query(Listing).filter(
        Listing.asset_type == "cask",
        Listing.status == "active",
    ).all()

    return [
        {
            "id": l.id,
            "asset_type": l.asset_type,
            "title": l.title,
            "seller_type": l.seller_type,
            "market": l.market,
            "price_gbp": l.price_gbp,
            "status": l.status,
        }
        for l in listings
    ]


@router.post("/buy/{listing_id}")
def buy_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.status != "active":
        raise HTTPException(status_code=400, detail="Listing is not active")

    listing.status = "sold"

    db.add(listing)
    db.commit()
    db.refresh(listing)

    return {
        "message": "Purchase completed",
        "listing_id": listing.id,
        "buyer_id": current_user.id,
        "status": listing.status,
    }