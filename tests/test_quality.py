from datetime import date

from spm.data.normalized import MatchRecord
from spm.data.quality import validate_records


def test_quality_flags_future_partial_and_duplicates() -> None:
    records = [
        MatchRecord(date(2026, 8, 9), "A", "B", 1, None),
        MatchRecord(date(2026, 8, 8), "A", "B", 1, 0),
        MatchRecord(date(2026, 8, 8), "A", "B", 1, 0),
    ]
    issues = validate_records(records, as_of=date(2026, 8, 8))
    codes = [issue.code for issue in issues]
    assert "future_record" in codes
    assert "partial_score" in codes
    assert "duplicate_identity" in codes
