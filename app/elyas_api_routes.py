from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

def now_iso():
    return datetime.now(timezone.utc).isoformat()

CASKS = [
    {
        "id": 1,
        "cask_code": "HH-2023-0847",
        "distillery": "Ardbeg",
        "warehouse": "WH-03 Islay",
        "cask_type": "Oloroso Sherry Hogshead",
        "wood_origin": "European Oak",
        "size_liters": 250,
        "purchase_price_gbp": 38500,
        "current_value_gbp": 45200,
        "projected_value_gbp": 124000,
        "maturation_score": 88,
        "risk_score": 12,
        "abv": 63.2,
        "fill_level": 94.1,
        "temperature_c": 12.4,
        "humidity_pct": 68,
        "lbb_device_id": "LBB-2026-0847",
        "status": "maturing",
        "owner_id": 1,
        "region": "Islay"
    },
    {
        "id": 2,
        "cask_code": "BN-2024-1205",
        "distillery": "Bunnahabhain",
        "warehouse": "WH-01 Islay",
        "cask_type": "Ex-Bourbon Barrel",
        "wood_origin": "American Oak",
        "size_liters": 200,
        "purchase_price_gbp": 32800,
        "current_value_gbp": 38500,
        "projected_value_gbp": 99000,
        "maturation_score": 81,
        "risk_score": 18,
        "abv": 61.8,
        "fill_level": 95.0,
        "temperature_c": 12.7,
        "humidity_pct": 66,
        "lbb_device_id": "LBB-2026-1205",
        "status": "maturing",
        "owner_id": 1,
        "region": "Islay"
    },
    {
        "id": 3,
        "cask_code": "LP-2025-0332",
        "distillery": "Laphroaig",
        "warehouse": "WH-04 Islay",
        "cask_type": "Quarter Cask",
        "wood_origin": "American Oak",
        "size_liters": 125,
        "purchase_price_gbp": 35400,
        "current_value_gbp": 41000,
        "projected_value_gbp": 119000,
        "maturation_score": 84,
        "risk_score": 14,
        "abv": 62.4,
        "fill_level": 94.8,
        "temperature_c": 12.2,
        "humidity_pct": 69,
        "lbb_device_id": "LBB-2026-0332",
        "status": "maturing",
        "owner_id": 1,
        "region": "Islay"
    }
]

TRANSACTIONS = [
    {"id": 1, "asset_type": "cask", "listing_id": 1, "amount_gbp": 45200, "status": "completed", "created_at": now_iso()},
    {"id": 2, "asset_type": "cask", "listing_id": 5, "amount_gbp": 38500, "status": "completed", "created_at": now_iso()}
]

ORDERS = [
    {"id": "ORD-001", "symbol": "CASK-1", "side": "BUY", "price_gbp": 43800, "quantity": 1, "status": "open", "created_at": now_iso()},
    {"id": "ORD-002", "symbol": "CASK-1", "side": "SELL", "price_gbp": 46200, "quantity": 1, "status": "open", "created_at": now_iso()}
]

TRADES = [
    {"id": "TRD-001", "symbol": "CASK-1", "price_gbp": 42900, "quantity": 1, "buyer": "Demo Buyer", "seller": "Demo Seller", "status": "completed", "created_at": now_iso()}
]

class OrderCreate(BaseModel):
    symbol: str
    side: str
    price_gbp: float
    quantity: int = 1

@router.get("/health")
def health():
    return {"status": "ok", "service": "E.L.Y.A.S.-A.I. API", "time": now_iso()}

@router.get("/status")
def status():
    return {"status": "live", "backend": "Railway", "api": "v1", "time": now_iso()}

@router.get("/me")
def me():
    return {
        "id": 1,
        "email": "demo@investor.com",
        "full_name": "Demo Investor",
        "role": "investor",
        "permissions": ["portfolio:read", "casks:read", "marketplace:read", "transactions:read", "monitoring:read"]
    }

@router.get("/casks")
def get_casks():
    return CASKS

@router.get("/casks/{cask_id}")
def get_cask(cask_id: int):
    for cask in CASKS:
        if int(cask["id"]) == int(cask_id):
            return cask
    raise HTTPException(status_code=404, detail="Cask not found")

@router.get("/portfolio/summary")
def portfolio_summary():
    total_current = sum(float(c.get("current_value_gbp", 0)) for c in CASKS)
    total_projected = sum(float(c.get("projected_value_gbp", 0)) for c in CASKS)
    total_purchase = sum(float(c.get("purchase_price_gbp", 0)) for c in CASKS)
    avg_maturation = sum(float(c.get("maturation_score", 0)) for c in CASKS) / max(len(CASKS), 1)
    roi = ((total_projected - total_current) / total_current * 100) if total_current else 0
    return {
        "total_casks": len(CASKS),
        "total_current_value": total_current,
        "total_projected_value": total_projected,
        "total_purchase_value": total_purchase,
        "unrealized_pnl": total_current - total_purchase,
        "roi": roi,
        "average_maturation_score": avg_maturation,
        "liquidity_score": 82,
        "ai_confidence_pct": 94
    }

@router.get("/transactions/my")
def my_transactions():
    return TRANSACTIONS

@router.get("/monitoring/casks")
def monitoring_casks():
    return [
        {
            "id": c["id"],
            "cask_code": c["cask_code"],
            "distillery": c["distillery"],
            "lbb_device_id": c["lbb_device_id"],
            "temperature_c": c["temperature_c"],
            "humidity_pct": c["humidity_pct"],
            "fill_level": c["fill_level"],
            "status": "online",
            "last_reading": now_iso()
        }
        for c in CASKS
    ]

@router.get("/monitoring/telemetry/{cask_id}")
def telemetry(cask_id: str):
    cask = None
    for item in CASKS:
        if str(item["id"]) == str(cask_id) or str(item["cask_code"]) == str(cask_id):
            cask = item
            break
    if not cask:
        raise HTTPException(status_code=404, detail="Telemetry not found")
    return {
        "cask_id": cask["id"],
        "cask_code": cask["cask_code"],
        "device_id": cask["lbb_device_id"],
        "temperature_c": cask["temperature_c"],
        "humidity_pct": cask["humidity_pct"],
        "fill_level_pct": cask["fill_level"],
        "abv": cask["abv"],
        "air_quality": "optimal",
        "vibration_g": 0.1,
        "last_reading": now_iso(),
        "points": [
            {"t": "09:00", "temperature_c": cask["temperature_c"] - 0.1, "humidity_pct": cask["humidity_pct"]},
            {"t": "10:00", "temperature_c": cask["temperature_c"], "humidity_pct": cask["humidity_pct"]},
            {"t": "11:00", "temperature_c": cask["temperature_c"] + 0.1, "humidity_pct": cask["humidity_pct"] - 1},
            {"t": "12:00", "temperature_c": cask["temperature_c"], "humidity_pct": cask["humidity_pct"]}
        ]
    }

@router.get("/dashboard/{role}")
def dashboard(role: str):
    if role == "investor":
        summary = portfolio_summary()
        return {"role": "investor", "total_nav_gbp": summary["total_current_value"], "projected_exit_gbp": summary["total_projected_value"], "unrealized_pnl_gbp": summary["unrealized_pnl"], "liquidity_score": 82, "ai_confidence_pct": 94, "holdings": CASKS, "generated_at": now_iso()}
    if role == "broker":
        return {"role": "broker", "managed_aum_gbp": 4820000, "authorised_clients": 38, "monitored_casks": 214, "pending_otc_gbp": 682000, "commission_mtd_gbp": 18400, "generated_at": now_iso()}
    if role == "distillery":
        return {"role": "distillery", "warehouse_casks": 8420, "lbb_devices": 1284, "direct_shop_revenue_gbp": 312000, "erp_status": "healthy", "release_pipeline": 17, "generated_at": now_iso()}
    if role in ["private-seller", "private"]:
        return {"role": "private-seller", "owned_assets": 9, "estimated_value_gbp": 286000, "sale_ready": 4, "offers_received": 12, "ai_sell_score": 86, "generated_at": now_iso()}
    if role == "admin":
        return {"role": "admin", "users": 42, "casks": len(CASKS), "trades": len(TRADES), "orders": len(ORDERS), "generated_at": now_iso()}
    raise HTTPException(status_code=404, detail="Dashboard role not found")

@router.get("/netsuite/status")
def netsuite_status():
    return {"status": "healthy", "connector": "ready", "queue_depth": 4, "last_sync": now_iso(), "modules": ["inventory", "production_batches", "sales_orders", "invoices", "commission_accounting"]}

@router.post("/netsuite/sync")
def netsuite_sync(payload: Optional[Dict[str, Any]] = None):
    return {"status": "completed", "processed": 4, "failed": 0, "completed_at": now_iso(), "payload": payload or {}}

@router.get("/ai/valuation/{asset_id}")
def ai_valuation(asset_id: str):
    cask = None
    for item in CASKS:
        if str(item["id"]) == str(asset_id) or str(item["cask_code"]) == str(asset_id):
            cask = item
            break
    if not cask:
        return {"asset_id": asset_id, "fair_value_gbp": 0, "confidence_pct": 0, "liquidity_score": 0, "recommendation": "REVIEW", "thesis": "Asset not found. Verification required."}
    return {"asset_id": asset_id, "fair_value_gbp": cask["current_value_gbp"], "projected_value_gbp": cask["projected_value_gbp"], "confidence_pct": 94, "liquidity_score": 82, "recommendation": "HOLD", "thesis": "Strong maturation trajectory, favourable warehouse conditions and rising Islay demand."}

@router.get("/ai/signals")
def ai_signals():
    return [
        {"type": "market", "severity": "positive", "message": "Islay cask demand remains strong."},
        {"type": "valuation", "severity": "positive", "message": "Verified assets are pricing above non-monitored assets."},
        {"type": "liquidity", "severity": "info", "message": "Average spread remains institutional-grade."},
        {"type": "monitoring", "severity": "info", "message": "Leonardo Black Box linked casks show lower buyer risk discount."}
    ]

@router.get("/orders")
def get_orders():
    return ORDERS

@router.post("/orders")
def place_order(order: OrderCreate):
    new_order = {"id": f"ORD-{len(ORDERS) + 1:03d}", "symbol": order.symbol, "side": order.side.upper(), "price_gbp": order.price_gbp, "quantity": order.quantity, "status": "open", "created_at": now_iso()}
    ORDERS.append(new_order)
    return new_order

@router.get("/trades")
def get_trades():
    return TRADES
