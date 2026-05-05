from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Cask(Base):
    __tablename__ = "casks"

    id = Column(Integer, primary_key=True, index=True)
    cask_code = Column(String(80), unique=True, index=True, nullable=False)

    distillery = Column(String(120), nullable=False)
    warehouse = Column(String(120), nullable=True)
    cask_type = Column(String(120), nullable=True)
    wood_origin = Column(String(120), nullable=True)

    size_liters = Column(Float, default=250)

    current_value_gbp = Column(Float, default=0)
    purchase_price_gbp = Column(Float, default=0)
    projected_value_gbp = Column(Float, default=0)

    maturation_score = Column(Float, default=0)
    risk_score = Column(Float, default=0)

    abv = Column(Float, default=0)
    fill_level = Column(Float, default=100)

    temperature_c = Column(Float, default=12.4)
    humidity_pct = Column(Float, default=68)

    lbb_device_id = Column(String(120), nullable=True)
    status = Column(String(50), default="maturing")

    # 🔥 RELAZIONE CORRETTA
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="casks")

    created_at = Column(DateTime(timezone=True), server_default=func.now())