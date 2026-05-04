from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.db.session import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    asset_type = Column(String(50), nullable=False)  # cask, bottle, service
    title = Column(String(255), nullable=False)
    seller_type = Column(String(50), default="distillery")  # distillery, broker, collector
    market = Column(String(50), default="exchange")  # exchange, shop, b2b, b2c
    price_gbp = Column(Float, default=0)
    quantity = Column(Integer, default=1)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
