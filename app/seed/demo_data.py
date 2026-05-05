from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.cask import Cask
from app.models.listing import Listing
from app.models.user import User


def seed_demo_data():
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == "demo@investor.com").first()
        if existing_user:
            return

        admin = User(
            email="admin@elyas-ai.com",
            full_name="E.L.Y.A.S. Admin",
            role="admin",
            hashed_password=hash_password("admin123"),
            is_active=True,
        )
        db.add(admin)
        db.flush()

        user1 = User(
            email="demo@investor.com",
            full_name="John Smith",
            role="client",
            hashed_password=hash_password("demo123"),
            is_active=True,
        )
        db.add(user1)
        db.flush()

        user2 = User(
            email="broker@elyas-ai.com",
            full_name="Broker Client",
            role="client",
            hashed_password=hash_password("demo123"),
            is_active=True,
        )
        db.add(user2)
        db.flush()

        casks = [
            Cask(
                cask_code="HH-2023-0847",
                distillery="Ardbeg",
                warehouse="WH-03 Islay",
                cask_type="Oloroso Sherry",
                wood_origin="European Oak",
                size_liters=250,
                current_value_gbp=45200,
                purchase_price_gbp=38000,
                projected_value_gbp=125000,
                maturation_score=87,
                risk_score=14,
                abv=58.3,
                fill_level=94.2,
                temperature_c=12.4,
                humidity_pct=68,
                lbb_device_id="LBB-2026-0847",
                status="maturing",
                owner_id=user1.id,
            ),
            Cask(
                cask_code="BN-2024-1205",
                distillery="Bunnahabhain",
                warehouse="WH-01 Islay",
                cask_type="Ex-Bourbon",
                wood_origin="American Oak",
                size_liters=200,
                current_value_gbp=38500,
                purchase_price_gbp=34300,
                projected_value_gbp=98000,
                maturation_score=82,
                risk_score=18,
                abv=59.1,
                fill_level=96.1,
                temperature_c=12.7,
                humidity_pct=67,
                lbb_device_id="LBB-2026-1205",
                status="maturing",
                owner_id=user1.id,
            ),
            Cask(
                cask_code="LP-2025-0332",
                distillery="Laphroaig",
                warehouse="WH-05 Islay",
                cask_type="Quarter Cask",
                wood_origin="American Oak",
                size_liters=125,
                current_value_gbp=41000,
                purchase_price_gbp=37800,
                projected_value_gbp=119000,
                maturation_score=79,
                risk_score=22,
                abv=60.2,
                fill_level=97.0,
                temperature_c=12.2,
                humidity_pct=69,
                lbb_device_id="LBB-2027-0332",
                status="maturing",
                owner_id=user2.id,
            ),
        ]

        db.add_all(casks)

        listings = [
            Listing(
                asset_type="cask",
                title="Ardbeg 2023 Oloroso Hogshead",
                seller_type="broker",
                market="exchange",
                price_gbp=45200,
            ),
            Listing(
                asset_type="cask",
                title="Macallan 2022 Sherry Butt",
                seller_type="distillery",
                market="exchange",
                price_gbp=92000,
            ),
            Listing(
                asset_type="bottle",
                title="Limited Single Cask Release 1998",
                seller_type="collector",
                market="exchange",
                price_gbp=2800,
            ),
            Listing(
                asset_type="bottle",
                title="Distillery Direct Premium Release",
                seller_type="distillery",
                market="shop",
                price_gbp=185,
            ),
        ]

        db.add_all(listings)
        db.commit()

    finally:
        db.close()