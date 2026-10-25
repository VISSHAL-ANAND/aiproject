# Runtime Flow (Tier 2)

1. Browser map starts at a demo coordinate.
2. User clicks a point or requests GPS.
3. Frontend sends latitude/longitude to POST /api/predict.
4. Pydantic validates coordinates.
5. Provider services concurrently fetch Open-Meteo weather and Nominatim reverse geocoding.
6. Baseline service scores available inputs and explains contributing factors.
7. Response returns score, level, location label, weather summary, recommendations, and disclaimer.
8. Frontend escapes provider strings before rendering.

Historical hotspots are exposed through GET /api/hotspots; rendering that layer on the map remains a follow-up task.
