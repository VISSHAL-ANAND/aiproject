# AI-Based Road Accident Risk Prediction

College-project prototype for location-aware road risk assessment using current weather, road context, time, and optional historical accident records. The initial score is a transparent **risk index**, not a calibrated probability of a future accident.

## Features
- Leaflet/OpenStreetMap map with click-to-select and browser GPS.
- Reverse geocoding and current weather via OpenStreetMap Nominatim and Open-Meteo.
- Explainable baseline risk score, level, and safety guidance.
- Optional historical accident CSV loader.
- FastAPI backend, OpenAPI docs, model-training scaffold, tests, and structured documentation.

## Run
Python 3.10+ recommended.
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs. GPS requires localhost/HTTPS and browser permission.

## Data and ML
No fabricated accident data is bundled. See `data/README.md`. The training script requires a suitable labeled dataset; accident and non-accident observations must represent real exposure windows. Use temporal and geographic holdouts and calibration before claiming probability. Runtime is not yet wired to a trained model.

## Tests
```bash
python -m pytest
```

## Endpoints
- `GET /api/health`
- `GET /api/context?lat=...&lon=...`
- `POST /api/predict`
- `GET /api/hotspots`

## Structure
`app/` API, services, static frontend · `scripts/` training · `tests/` tests · `data/` dataset instructions · `DOX/` requested documentation pack.

## Limitations and privacy
A score of 72/100 does not mean a 72% accident probability. Provider data can be missing or stale; no live traffic source is currently integrated. GPS is permission-based and coordinates are sent to external weather/geocoding providers. OpenStreetMap attribution is shown in the UI. Do not use this prototype as emergency or guaranteed safety advice.
