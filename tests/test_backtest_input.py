from datetime import date

from spm.data.normalized import MatchRecord
from spm.ingestion.backtest_input import to_backtest_matches


def test_normalized_records_are_converted_for_backtest():
    records = [
        MatchRecord(date(2025, 8, 2), "B", "C", 2, 1, "I1", "2526"),
        MatchRecord(date(2025, 8, 1), "A", "B", 1, 1, "I1", "2526"),
        MatchRecord(date(2025, 8, 3), "C", "D", None, None, "I1", "2526"),
    ]
    matches = to_backtest_matches(records)
    assert len(matches) == 2
    assert matches[0].home_team == "A"
    assert matches[1].home_team == "B"
