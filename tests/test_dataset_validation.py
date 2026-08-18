from datetime import date

from spm.data.normalized import MatchRecord
from spm.ingestion.validation import validate_historical_dataset


def test_validation_removes_incomplete_and_duplicate_records():
    complete = MatchRecord(date(2025, 8, 1), "A", "B", 1, 0, "I1", "2526")
    duplicate = MatchRecord(date(2025, 8, 1), "A", "B", 1, 0, "I1", "2526")
    incomplete = MatchRecord(date(2025, 8, 2), "C", "D", None, None, "I1", "2526")
    result = validate_historical_dataset([incomplete, duplicate, complete])
    assert result == (complete,)
