from pydantic import BaseModel


class CaskOut(BaseModel):
    id: int
    cask_code: str
    distillery: str
    warehouse: str | None
    cask_type: str | None
    current_value_gbp: float
    projected_value_gbp: float
    maturation_score: float
    risk_score: float
    abv: float
    fill_level: float
    temperature_c: float
    humidity_pct: float
    lbb_device_id: str | None
    status: str

    class Config:
        from_attributes = True


class PortfolioSummary(BaseModel):
    total_value_gbp: float
    total_projected_value_gbp: float
    number_of_casks: int
    average_maturation_score: float
    average_roi_pct: float
