from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func

from app.db.session import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    transaction_type = Column(String(50), default="purchase")
    asset_type = Column(String(50), nullable=False)
    asset_id = Column(Integer, nullable=True)
    listing_id = Column(Integer, nullable=True)

    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    amount_gbp = Column(Float, default=0)
    status = Column(String(50), default="completed")

    created_at = Column(DateTime(timezone=True), server_default=func.now())