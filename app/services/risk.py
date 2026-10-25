from app.schemas import PredictionRequest, PredictionResponse, RiskFactor

def assess_risk(data: PredictionRequest, location_label: str | None = None,
                weather_summary: str | None = None) -> PredictionResponse:
    """Transparent baseline index; replace only after valid model evaluation."""
    score = 12
    factors: list[RiskFactor] = []
    recs: list[str] = []
    weather = (data.weather or "").lower()
    if any(x in weather for x in ("rain", "drizzle", "thunder", "snow")):
        score += 18
        factors.append(RiskFactor(name="Adverse weather", impact="high", detail="Reported weather may reduce grip or visibility."))
        recs.append("Reduce speed and increase following distance in adverse weather.")
    if data.precipitation_mm is not None and data.precipitation_mm > 0:
        score += min(14, int(data.precipitation_mm * 2))
        factors.append(RiskFactor(name="Precipitation", impact="medium", detail=f"Precipitation reported: {data.precipitation_mm:g} mm."))
    if data.visibility_m is not None and data.visibility_m < 1000:
        score += 18
        factors.append(RiskFactor(name="Low visibility", impact="high", detail="Visibility below 1 km was supplied."))
        recs.append("Use appropriate lights and avoid sudden manoeuvres.")
    if data.is_night:
        score += 10
        factors.append(RiskFactor(name="Night-time", impact="medium", detail="Reduced visibility and fatigue may increase driving demands."))
    if (data.traffic_level or "").lower() in {"heavy", "high"}:
        score += 12
        factors.append(RiskFactor(name="Heavy traffic", impact="medium", detail="Heavy traffic level was supplied by the caller."))
    if (data.road_type or "").lower() in {"unlit", "sharp_curve", "poor_surface"}:
        score += 12
        factors.append(RiskFactor(name="Road characteristic", impact="medium", detail=f"Potentially hazardous road attribute: {data.road_type}."))
    if data.historical_incidents:
        score += min(20, data.historical_incidents * 2)
        factors.append(RiskFactor(name="Historical incidents", impact="medium", detail=f"{data.historical_incidents} nearby recorded incidents supplied."))
    score = max(0, min(100, score))
    level = "LOW" if score < 30 else "MEDIUM" if score < 60 else "HIGH"
    if not recs:
        recs.append("Follow posted speed limits, maintain distance, and stay alert.")
    return PredictionResponse(lat=data.lat, lon=data.lon, risk_score=score, risk_level=level,
        location_label=location_label, weather_summary=weather_summary, factors=factors,
        recommendations=recs)
