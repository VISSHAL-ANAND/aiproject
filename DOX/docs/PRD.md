# Product Requirements (Tier 2)

## Primary flow
User selects a point or grants geolocation permission. The app fetches context, weather, and optional historical incidents; it returns a score, level, factors, recommendations, and limitations.

## Functional requirements
- FR-1: map selection and browser geolocation with explicit permission.
- FR-2: validate coordinates at API boundary.
- FR-3: retrieve weather and reverse geocode with timeouts and graceful fallback.
- FR-4: provide transparent baseline score, not a probability claim.
- FR-5: optionally load documented accident CSV records; never synthesize missing events.
- FR-6: provide health and OpenAPI endpoints.
- FR-7: provide reproducible training scaffold and evaluation warnings.
- FR-8: document limitations and data provenance.

## Quality requirements
Accessible controls, responsive layout, escaped UI text, no secrets in source. External provider errors must not crash the application. Production ML claims require temporal and geographic validation.

## Acceptance
Clean install, healthy API, bounded score, graceful missing-data handling, and passing tests.
