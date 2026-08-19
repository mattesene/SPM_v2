from datetime import date

import pytest

from spm.data.odds import DrawOdds, index_draw_odds
from spm.data.odds_csv import DrawOddsCSVImporter


def test_draw_odds_rejects_invalid_price():
    with pytest.raises(ValueError):
        DrawOdds(date(2026, 8, 1), "Inter", "Milan", 1.0)


def test_draw_odds_index_rejects_conflicting_duplicate():
    first = DrawOdds(date(2026, 8, 1), "Inter", "Milan", 3.1)
    second = DrawOdds(date(2026, 8, 1), "Inter", "Milan", 3.2)
    with pytest.raises(ValueError):
        index_draw_odds([first, second])


def test_draw_odds_csv_importer(tmp_path):
    path = tmp_path / "odds.csv"
    path.write_text(
        "Date,HomeTeam,AwayTeam,DrawOdds\n01/08/2026,Inter,Milan,3.25\n",
        encoding="utf-8",
    )
    records = DrawOddsCSVImporter().load(path)
    assert records[0].date == date(2026, 8, 1)
    assert records[0].draw_odds == 3.25
