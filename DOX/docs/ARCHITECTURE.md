# Architecture

```
Leaflet browser UI
  | POST /api/predict
FastAPI + Pydantic validation
  |-- weather provider: Open-Meteo
  |-- reverse geocoder: Nominatim
  |-- risk service: transparent heuristic baseline
  |-- hotspot service: optional local CSV
Offline training script -> model artifact (not wired into runtime)
```

Services are separate from HTTP routes to ease replacement and testing. The baseline is deterministic and explainable. A future model must share the training/runtime feature contract and retain fallback behavior.
