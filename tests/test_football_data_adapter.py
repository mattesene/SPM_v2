from datetime import date
from io import StringIO

from spm.ingestion.football_data import FootballDataAdapter


def test_football_data_row_normalization() -> None:
    retrieved = __import__("datetime").datetime(2026, 8, 9)
    record = FootballDataAdapter._record(
        {"Date": "09/08/26", "HomeTeam": " Inter ", "AwayTeam": "Milan", "FTHG": "2", "FTAG": "1"},
        "https://example.test/I1.csv",
        retrieved,
        "2526",
        "I1",
    )
    assert record.date == date(2026, 8, 9)
    assert record.home_team == "Inter"
    assert record.away_goals == 1
    assert record.completed
    assert record.provenance[0].source == "football-data"
