# Security and Privacy

- Never commit .env, API keys, credentials, or private datasets.
- Browser GPS requires permission; provide map selection as alternative.
- Coordinates are sent to weather/geocoding providers; disclose this before public deployment.
- Use HTTPS outside localhost. Restrict CORS and add rate limiting before deployment.
- Escape user/provider strings before HTML insertion.
- Do not collect or store precise location histories by default.
- Review OpenStreetMap, Nominatim, and weather-provider terms and attribution.
- Do not present this educational prototype as emergency advice or a safety guarantee.
