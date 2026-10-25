# State / Handoff (Tier 1)

## Current state
- FastAPI prototype with Leaflet UI, browser geolocation, map selection, Open-Meteo weather, Nominatim reverse geocoding, baseline index, optional CSV hotspot loading.
- Training scaffold exists; runtime prediction is **not connected to a trained model**.
- No real accident dataset is bundled.
- Risk output is a heuristic index, not a probability.
- Run tests with `python -m pytest`.

## Current focus
1. Verify clean install, app startup, and browser UI.
2. Find a legally usable dataset for the chosen pilot geography.
3. Define accident/non-accident exposure labels and prediction horizon before training.
4. Add time/geographic holdout evaluation and calibration.
5. Connect a model only after evaluation and input-schema parity checks.

Update this file after significant work; record verified facts only.
