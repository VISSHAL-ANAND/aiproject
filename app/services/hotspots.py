import csv
from pathlib import Path

DATA_PATH = Path("data/accidents.csv")

def load_hotspots(path: Path = DATA_PATH) -> list[dict]:
    """Load optional cleaned records; absent data means no hotspots, not fake examples."""
    if not path.exists():
        return []
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            try:
                lat, lon = float(row["latitude"]), float(row["longitude"])
            except (KeyError, TypeError, ValueError):
                continue
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                continue
            rows.append({"lat": lat, "lon": lon, "date": row.get("date"), "severity": row.get("severity"), "description": row.get("description")})
    return rows
