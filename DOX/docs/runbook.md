# Runbook

## Local startup
Create a virtual environment, install requirements.txt, run `uvicorn app.main:app --reload`.

## Health check
Open `/api/health`; expected response includes `"status":"ok"`.

## Troubleshooting
- Map blank: check internet and browser console; tiles are external.
- Weather unavailable: check Open-Meteo; baseline prediction should still work.
- GPS unavailable: use localhost/HTTPS, grant permission, or click map.
- Geocoding unavailable: selected coordinates remain usable.
- No hotspots: provide cleaned `data/accidents.csv`; no demo incidents are invented.

## Before demo
Run tests, check API docs, test GPS permission denial and provider outage, and explain risk-index limitations.
