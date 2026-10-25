from app.schemas import PredictionRequest
from app.services.risk import assess_risk

def test_score_bounded():
    result = assess_risk(PredictionRequest(lat=11, lon=76, weather="Rain", precipitation_mm=8, visibility_m=300, is_night=True, traffic_level="heavy", historical_incidents=20))
    assert 0 <= result.risk_score <= 100
    assert result.risk_level in {"LOW", "MEDIUM", "HIGH"}

def test_clear_baseline_has_guidance():
    result = assess_risk(PredictionRequest(lat=11, lon=76, weather="Clear"))
    assert result.recommendations
    assert result.score_type == "baseline_index"

def test_coordinates_preserved():
    result = assess_risk(PredictionRequest(lat=12.5, lon=77.6))
    assert result.lat == 12.5 and result.lon == 77.6
