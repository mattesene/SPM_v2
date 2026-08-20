from datetime import date

from spm.data.match_conversion import to_completed_matches
from spm.data.normalized import MatchRecord


def test_to_completed_matches_filters_unfinished_and_canonicalizes():
    rows = [
        MatchRecord(date(2020, 2, 1), "Man Utd", "Chelsea", 1, 1),
        MatchRecord(date(2020, 1, 1), "Arsenal", "Chelsea"),
    ]
    matches = to_completed_matches(rows)
    assert len(matches) == 1
    assert matches[0].is_draw
