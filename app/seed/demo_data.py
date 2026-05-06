from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.cask import Cask
from app.models.listing import Listing
from app.models.user import User


def get_or_create_user(db, email, full_name, role, password):
    user = db.query(User).filter(User.email == email).first()

    if user:
        user.full_name = full_name
        user.role = role
        user.hashed_password = get_password_hash(password)
        user.is_active = True
        db.add(user)
        db.flush()
        return user

    user = User(
        email=email,
        full_name=full_name,
        role=role,
        hashed_password=get_password_hash(password),
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


def get_or_create_cask(
    db,
    cask_code,
    distillery,
    warehouse,
    cask_type,
    wood_origin,
    size_liters,
    current_value_gbp,
    purchase_price_gbp,
    projected_value_gbp,
    maturation_score,
    risk_score,
    abv,
    fill_level,
    temperature_c,
    humidity_pct,
    lbb_device_id,
    status,
    owner_id,
):
    cask = db.query(Cask).filter(Cask.cask_code == cask_code).first()

    if cask:
        cask.distillery = distillery
        cask.warehouse = warehouse
        cask.cask_type = cask_type
        cask.wood_origin = wood_origin
        cask.size_liters = size_liters
        cask.current_value_gbp = current_value_gbp
        cask.purchase_price_gbp = purchase_price_gbp
        cask.projected_value_gbp = projected_value_gbp
        cask.maturation_score = maturation_score
        cask.risk_score = risk_score
        cask.abv = abv
        cask.fill_level = fill_level
        cask.temperature_c = temperature_c
        cask.humidity_pct = humidity_pct
        cask.lbb_device_id = lbb_device_id
        cask.status = status
        cask.owner_id = owner_id
        db.add(cask)
        db.flush()
        return cask

    cask = Cask(
        cask_code=cask_code,
        distillery=distillery,
        warehouse=warehouse,
        cask_type=cask_type,
        wood_origin=wood_origin,
        size_liters=size_liters,
        current_value_gbp=current_value_gbp,
        purchase_price_gbp=purchase_price_gbp,
        projected_value_gbp=projected_value_gbp,
        maturation_score=maturation_score,
        risk_score=risk_score,
        abv=abv,
        fill_level=fill_level,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        lbb_device_id=lbb_device_id,
        status=status,
        owner_id=owner_id,
    )
    db.add(cask)
    db.flush()
    return cask


def get_or_create_listing(
    db,
    title,
    asset_type,
    seller_type,
    market,
    price_gbp,
    cask_id=None,
    status="active",
):
    listing = db.query(Listing).filter(Listing.title == title).first()

    if listing:
        listing.asset_type = asset_type
        listing.seller_type = seller_type
        listing.market = market
        listing.price_gbp = price_gbp
        listing.cask_id = cask_id
        listing.status = status
        db.add(listing)
        db.flush()
        return listing

    listing = Listing(
        asset_type=asset_type,
        title=title,
        seller_type=seller_type,
        market=market,
        price_gbp=price_gbp,
        cask_id=cask_id,
        status=status,
    )
    db.add(listing)
    db.flush()
    return listing


def seed_demo_data():
    db = SessionLocal()

    try:
        admin = get_or_create_user(
            db=db,
            email="admin@elyas-ai.com",
            full_name="E.L.Y.A.S. Admin",
            role="admin",
            password="admin123",
        )

        user1 = get_or_create_user(
            db=db,
            email="demo@investor.com",
            full_name="John Smith",
            role="client",
            password="demo123",
        )

        user2 = get_or_create_user(
            db=db,
            email="broker@elyas-ai.com",
            full_name="Broker Client",
            role="client",
            password="demo123",
        )

        cask1 = get_or_create_cask(
            db=db,
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
        )

        cask2 = get_or_create_cask(
            db=db,
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
        )

        cask3 = get_or_create_cask(
            db=db,
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
        )

        get_or_create_listing(
            db=db,
            title="Ardbeg 2023 Oloroso Hogshead",
            asset_type="cask",
            seller_type="broker",
            market="exchange",
            price_gbp=45200,
            cask_id=cask1.id,
            status="active",
        )

        get_or_create_listing(
            db=db,
            title="Bunnahabhain 2024 Ex-Bourbon",
            asset_type="cask",
            seller_type="broker",
            market="exchange",
            price_gbp=38500,
            cask_id=cask2.id,
            status="active",
        )

        get_or_create_listing(
            db=db,
            title="Laphroaig 2025 Quarter Cask",
            asset_type="cask",
            seller_type="broker",
            market="exchange",
            price_gbp=41000,
            cask_id=cask3.id,
            status="active",
        )

        get_or_create_listing(
            db=db,
            title="Distillery Direct Premium Release",
            asset_type="bottle",
            seller_type="distillery",
            market="shop",
            price_gbp=185,
            cask_id=None,
            status="active",
        )

        db.commit()

    finally:
        db.close()