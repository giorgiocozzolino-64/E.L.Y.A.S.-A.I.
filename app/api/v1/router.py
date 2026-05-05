from fastapi import APIRouter

from app.api.v1 import admin, auth, casks, exchange, marketplace, portfolio, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(casks.router, prefix="/casks", tags=["Cask Monitoring"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(exchange.router, prefix="/exchange", tags=["Exchange"])
api_router.include_router(marketplace.router, prefix="/marketplace", tags=["Marketplace"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])