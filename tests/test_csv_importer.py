from io import StringIO

import pytest

from spm.data.csv_importer import import_matches_csv


CSV = """date,competition,season,home_team,away_team,home_goals,away_goals,draw_odds
2025-01-02,Serie A,2024-25,Internazionale Milano,AS Roma,1,1,3.20
2025-01-01,Serie A,2024-25,Milan,Lazio,2,0,3.10
"""


def test_csv_importer_normalizes_and_orders():
    result = import_matches_csv(StringIO(CSV))
    assert result[0].home_team == "milan"
    assert result[1].home_team == "inter"
    assert result[0].match_date < result[1].match_date
    assert result[1].draw_odds == 3.2


def test_csv_importer_requires_columns():
    with pytest.raises(ValueError, match="missing required columns"):
        import_matches_csv(StringIO("date,home_team\n2025-01-01,A\n"))
