from pathlib import Path

from spm.data.historical_catalog import HistoricalCatalog, HistoricalSource
from spm.data.historical_odds import load_historical_draw_odds


def test_load_historical_draw_odds(tmp_path: Path):
    source = HistoricalSource("E0", "2020-21", "x.csv", "https://example.invalid/x.csv")
    path = tmp_path / "E0" / "2020-21" / "x.csv"
    path.parent.mkdir(parents=True)
    path.write_text("Date,HomeTeam,AwayTeam,B365D\n01/08/20,A,B,3.20\n", encoding="utf-8")
    odds = load_historical_draw_odds(HistoricalCatalog((source,)), tmp_path)
    assert len(odds) == 1
    assert odds[0].draw_odds == 3.2
