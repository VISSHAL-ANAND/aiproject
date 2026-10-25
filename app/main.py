import asyncio
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.schemas import PredictionRequest, PredictionResponse
from app.services.providers import get_weather, reverse_geocode
from app.services.risk import assess_risk
from app.services.hotspots import load_hotspots

BASE_DIR = Path(__file__).parent
app = FastAPI(title=settings.app_name, version="0.1.0", description="Educational road risk index prototype.")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    return (BASE_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name}

@app.get("/api/context")
async def context(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180)):
    weather, place = await asyncio.gather(get_weather(lat, lon), reverse_geocode(lat, lon))
    return {"weather": weather, "location": place}

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    weather, place = await asyncio.gather(get_weather(request.lat, request.lon), reverse_geocode(request.lat, request.lon))
    merged = request.model_copy(update={
        "weather": request.weather or weather.get("weather"),
        "precipitation_mm": request.precipitation_mm if request.precipitation_mm is not None else weather.get("precipitation_mm")
    })
    return assess_risk(merged, place.get("label"), weather.get("summary"))

@app.get("/api/hotspots")
async def hotspots():
    items = load_hotspots()
    return {"count": len(items), "items": items, "source": "data/accidents.csv" if items else None}
