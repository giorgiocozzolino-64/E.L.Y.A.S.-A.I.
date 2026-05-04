from pydantic import BaseModel


class ListingOut(BaseModel):
    id: int
    asset_type: str
    title: str
    seller_type: str
    market: str
    price_gbp: float
    quantity: int
    status: str

    class Config:
        from_attributes = True
