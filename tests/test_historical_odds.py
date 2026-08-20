from pathlib import Path

from spm.data.historical_catalog import HistoricalCatalog
from spm.data.historical_odds import load_historical_draw_odds
from spm.data.season_urls import SeasonSource


def test_load_historical_draw_odds(tmp_path: Path):
    source = SeasonSource("E0", "2021", "https://example.invalid/x.csv", "x.csv")
    path = tmp_path / "E0" / "2021" / "x.csv"
    path.parent.mkdir(parents=True)
    path.write_text("Date,HomeTeam,AwayTeam,B365D\n01/08/20,A,B,3.20\n", encoding="utf-8")
    odds = load_historical_draw_odds(HistoricalCatalog((source,)), tmp_path)
    assert len(odds) == 1
    assert odds[0].draw_odds == 3.2
