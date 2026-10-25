from pathlib import Path
from app.services.hotspots import load_hotspots

def test_missing_file_returns_empty(tmp_path: Path):
    assert load_hotspots(tmp_path / "missing.csv") == []

def test_invalid_rows_are_skipped(tmp_path: Path):
    file = tmp_path / "accidents.csv"
    file.write_text("latitude,longitude,date\n999,2,2024-01-01\n11,76,2024-01-02\n", encoding="utf-8")
    rows = load_hotspots(file)
    assert len(rows) == 1 and rows[0]["lat"] == 11
