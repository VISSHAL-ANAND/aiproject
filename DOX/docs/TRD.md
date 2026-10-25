# Technical Requirements (Tier 2)

## Stack
Python 3.10+, FastAPI, Pydantic settings/schemas, HTTPX; Leaflet; Open-Meteo; Nominatim; pandas/scikit-learn; pytest.

## API
- GET /api/health
- GET /api/context?lat=&lon=
- POST /api/predict
- GET /api/hotspots

## ML contract
Define prediction horizon and target before fitting. Positive labels represent accidents in road-segment/time windows; negatives represent observed exposure windows without recorded accidents, not mutated accident rows. Split by time and geography; assess calibration. Training script is a scaffold, not proof of accuracy.

## External dependencies
Plan for provider outages, quotas, usage policy, and internet availability. Keep providers replaceable behind service functions.
