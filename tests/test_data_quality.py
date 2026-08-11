from datetime import date

from spm.data.normalized import MatchRecord
from spm.data.quality import validate_records


def test_quality_flags_duplicate_future_and_negative_score():
    first = MatchRecord(date(2026, 8, 1), "Team A", "Team B", 1, 0)
    duplicate = MatchRecord(date(2026, 8, 1), "Team A", "Team B", 1, 0)
    future = MatchRecord(date(2026, 8, 12), "Team C", "Team D", -1, 0)
    issues = validate_records([first, duplicate, future], as_of=date(2026, 8, 11))
    codes = {issue.code for issue in issues}
    assert {"duplicate_identity", "future_record", "negative_score"} <= codes


def test_quality_is_case_insensitive_for_same_team():
    record = MatchRecord(date(2026, 8, 1), "Team A", "team a", 0, 0)
    issues = validate_records([record])
    assert any(issue.code == "same_team" for issue in issues)
