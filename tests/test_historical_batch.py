from datetime import date

from spm.data.normalized import MatchRecord


def test_historical_batch_sort_key_is_deterministic():
    records = [
        MatchRecord(date(2025, 2, 1), "B", "C", 1, 0, "I1", "2526"),
        MatchRecord(date(2025, 1, 1), "A", "B", 0, 0, "E0", "2526"),
    ]
    ordered = sorted(records, key=lambda r: (r.competition, r.season, r.date, r.home_team, r.away_team))
    assert [r.competition for r in ordered] == ["E0", "I1"]
