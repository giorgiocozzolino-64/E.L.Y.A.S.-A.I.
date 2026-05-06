from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.cask import Cask
from app.models.listing import Listing
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.listing import ListingOut

router = APIRouter()


@router.get("/offers", response_model=list[ListingOut])
def marketplace_offers(db: Session = Depends(get_db)):
    return db.query(Listing).filter(
        Listing.market == "exchange",
        Listing.status == "active",
    ).all()


@router.get("/shop", response_model=list[ListingOut])
def online_shop(db: Session = Depends(get_db)):
    return db.query(Listing).filter(
        Listing.market == "shop",
        Listing.status == "active",
    ).all()


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
        raise HTTPException(status_code=400, detail="Listing not active")

    # CREATE TRANSACTION
    transaction = Transaction(
        buyer_id=current_user.id,
        listing_id=listing.id,
        amount_gbp=listing.price_gbp,
        asset_type=listing.asset_type,
        status="completed",
    )

    db.add(transaction)

    # TRANSFER OWNERSHIP IF CASK
    if listing.cask_id:
        cask = db.query(Cask).filter(Cask.id == listing.cask_id).first()

        if cask:
            cask.owner_id = current_user.id
            db.add(cask)

    # CLOSE LISTING
    listing.status = "sold"
    db.add(listing)

    db.commit()

    return {
        "message": "Purchase completed",
        "listing_id": listing.id,
        "buyer_id": current_user.id,
        "status": "sold",
    }