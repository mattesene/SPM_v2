from datetime import date

from spm.backtest.adapters import completed_matches
from spm.data.normalized import MatchRecord


def test_completed_matches_filters_unfinished_records():
    records = [
        MatchRecord(date(2025, 8, 1), "A", "B", 1, 1),
        MatchRecord(date(2025, 8, 2), "C", "D"),
    ]
    matches = completed_matches(records)
    assert len(matches) == 1
    assert matches[0].is_draw


def test_completed_matches_uses_canonical_names():
    records = [MatchRecord(date(2025, 8, 1), "Inter Milan", "AC Milan", 2, 0)]
    match = completed_matches(records)[0]
    assert match.home_team == "inter-milan"
    assert match.away_team == "ac-milan"
