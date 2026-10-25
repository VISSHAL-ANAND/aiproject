from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    weather: str | None = None
    precipitation_mm: float | None = Field(default=None, ge=0)
    visibility_m: float | None = Field(default=None, ge=0)
    is_night: bool | None = None
    road_type: str | None = None
    traffic_level: str | None = None
    historical_incidents: int = Field(default=0, ge=0)

class RiskFactor(BaseModel):
    name: str
    impact: str
    detail: str

class PredictionResponse(BaseModel):
    lat: float
    lon: float
    risk_score: int
    risk_level: str
    score_type: str = "baseline_index"
    location_label: str | None = None
    weather_summary: str | None = None
    factors: list[RiskFactor]
    recommendations: list[str]
    disclaimer: str = "Relative risk index only; not a calibrated accident probability."
