import httpx
from app.config import settings

async def get_weather(lat: float, lon: float) -> dict:
    params = {"latitude": lat, "longitude": lon, "current": "temperature_2m,relative_humidity_2m,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m", "timezone": "auto"}
    try:
        async with httpx.AsyncClient(timeout=settings.weather_timeout_seconds) as client:
            response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
            response.raise_for_status()
            current = response.json().get("current", {})
        description = _weather_description(current.get("weather_code"))
        return {"available": True, "summary": description, "temperature_c": current.get("temperature_2m"),
                "precipitation_mm": current.get("precipitation"), "wind_speed_kmh": current.get("wind_speed_10m"),
                "weather": description, "source": "Open-Meteo"}
    except (httpx.HTTPError, ValueError, TypeError):
        return {"available": False, "summary": "Weather unavailable", "weather": None, "source": None}

async def reverse_geocode(lat: float, lon: float) -> dict:
    try:
        async with httpx.AsyncClient(timeout=settings.geocoding_timeout_seconds, headers={"User-Agent": settings.nominatim_user_agent}) as client:
            response = await client.get("https://nominatim.openstreetmap.org/reverse", params={"lat": lat, "lon": lon, "format": "jsonv2", "zoom": 18})
            response.raise_for_status()
            data = response.json()
        address = data.get("address", {})
        return {"available": True, "label": data.get("display_name"), "road": address.get("road"), "source": "OpenStreetMap Nominatim"}
    except (httpx.HTTPError, ValueError, TypeError):
        return {"available": False, "label": None, "road": None, "source": None}

def _weather_description(code: int | None) -> str:
    if code is None: return "Unknown"
    if code == 0: return "Clear"
    if code in (1, 2, 3): return "Cloudy"
    if code in (45, 48): return "Fog"
    if code in (51, 53, 55, 61, 63, 65, 80, 81, 82): return "Rain"
    if code in (71, 73, 75, 77, 85, 86): return "Snow"
    if code in (95, 96, 99): return "Thunderstorm"
    return "Variable"
