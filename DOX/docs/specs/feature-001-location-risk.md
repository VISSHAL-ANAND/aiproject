# Feature 001 — Location Risk Assessment

## User story
As a road user, I want to select my location and see known conditions and a transparent risk index.

## Inputs
Latitude/longitude; weather and precipitation when available; optional visibility, night flag, road type, traffic level, and historical incident count.

## Output
Score 0–100, LOW/MEDIUM/HIGH level, location/weather summary, contributing factors, safety recommendations, and disclaimer.

## Failure behavior
If weather or geocoding fails, continue with available inputs and mark unavailable information. Never invent live traffic. Missing historical data means no historical adjustment.

## Acceptance
Coordinates are validated; score remains bounded; response includes disclaimer and recommendations; absent CSV returns empty hotspots.
