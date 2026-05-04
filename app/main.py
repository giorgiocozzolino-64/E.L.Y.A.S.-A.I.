from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import Base, engine
from app.seed.demo_data import seed_demo_data

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="E.L.Y.A.S.-A.I. Spirits Tech Platform Backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringere in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_demo_data()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "platform": "E.L.Y.A.S.-A.I.",
        "status": "online",
        "vision": "Bloomberg for whisky assets",
        "docs": "/docs",
    }
