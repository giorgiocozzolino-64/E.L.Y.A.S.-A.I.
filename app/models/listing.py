from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func

from app.db.session import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)

    asset_type = Column(String(50), nullable=False)

    title = Column(String(255), nullable=False)

    seller_type = Column(String(50), default="distillery")

    market = Column(String(50), default="exchange")

    price_gbp = Column(Float, default=0)

    quantity = Column(Integer, default=1)

    status = Column(String(50), default="active")

    # NEW
    cask_id = Column(Integer, ForeignKey("casks.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())