from pathlib import Path

from spm.data.historical_catalog import HistoricalCatalog
from spm.data.historical_loader import load_catalog
from spm.data.season_urls import SeasonSource


def test_load_catalog_passes_source_metadata_to_provider(tmp_path: Path):
    csv = tmp_path / "e02425.csv"
    csv.write_text("Date,HomeTeam,AwayTeam,FTHG,FTAG\n01/08/24,A,B,1,0\n", encoding="utf-8")
    root = tmp_path / "cache" / "e0" / "2425"
    root.mkdir(parents=True)
    cached = root / "e02425.csv"
    cached.write_text(csv.read_text(encoding="utf-8"), encoding="utf-8")
    catalog = HistoricalCatalog((SeasonSource("e0", "2425", "https://example/e0.csv", "e02425.csv"),))
    datasets = load_catalog(catalog, tmp_path / "cache")
    assert len(datasets[("e0", "2425")]) == 1
    assert datasets[("e0", "2425")][0].competition == "e0"
    assert datasets[("e0", "2425")][0].season == "2425"
