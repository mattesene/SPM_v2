from datetime import date

from spm.data.normalized import MatchRecord
from spm.ingestion.historical_manifest import validate_coverage


def test_coverage_reports_missing_slices():
    rows = [MatchRecord(date(2025, 1, 1), "A", "B", 0, 0, "I1", "2526")]
    coverage = validate_coverage(rows)
    assert coverage.expected_slices == 84
    assert coverage.present_slices == 1
    assert ("E0", "1920") in coverage.missing_slices
    assert coverage.records == 1
