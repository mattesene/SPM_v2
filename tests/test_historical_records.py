from pathlib import Path

from spm.data.historical_records import load_historical_records
from spm.data.historical_catalog import HistoricalCatalog
from spm.data.season_urls import SeasonSource


def test_load_historical_records_flattens_and_sorts(monkeypatch, tmp_path: Path):
    source = SeasonSource("E0", "2021", "https://example.invalid/x.csv", "x.csv")
    catalog = HistoricalCatalog((source,))
    from spm.data import historical_records
    monkeypatch.setattr(historical_records, "load_catalog", lambda c, r: {
        ("E0", "2021"): [
            type("R", (), {"date": __import__("datetime").date(2021, 2, 1), "competition":"E0", "season":"2021", "home_team":"B", "away_team":"A"})(),
            type("R", (), {"date": __import__("datetime").date(2021, 1, 1), "competition":"E0", "season":"2021", "home_team":"A", "away_team":"B"})(),
        ]
    })
    rows = load_historical_records(catalog, tmp_path)
    assert [row.home_team for row in rows] == ["A", "B"]
