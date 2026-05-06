from datetime import datetime

from pydantic import BaseModel


class TransactionOut(BaseModel):
    id: int
    transaction_type: str
    asset_type: str
    asset_id: int | None = None
    listing_id: int | None = None
    buyer_id: int
    seller_id: int | None = None
    amount_gbp: float
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True