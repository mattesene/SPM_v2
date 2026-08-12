from datetime import date

import pytest

from spm.data.normalized import MatchRecord
from spm.data.quality import validate_records


def test_quality_flags_duplicate_and_future_record():
    first = MatchRecord(date(2026, 8, 1), "Team A", "Team B", 1, 0)
    duplicate = MatchRecord(date(2026, 8, 1), "Team A", "Team B", 1, 0)
    future = MatchRecord(date(2026, 8, 12), "Team C", "Team D", 2, 0)
    issues = validate_records([first, duplicate, future], as_of=date(2026, 8, 11))
    codes = {issue.code for issue in issues}
    assert {"duplicate_identity", "future_record"} <= codes


def test_normalized_record_rejects_negative_score():
    with pytest.raises(ValueError, match="cannot be negative"):
        MatchRecord(date(2026, 8, 12), "Team C", "Team D", -1, 0)


def test_quality_is_case_insensitive_for_same_team():
    record = MatchRecord(date(2026, 8, 1), "Team A", "team a", 0, 0)
    issues = validate_records([record])
    assert any(issue.code == "same_team" for issue in issues)
