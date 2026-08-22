from datetime import date

from spm.data.ingest_quality import apply_quality_gate
from spm.data.normalized import MatchRecord


def test_quality_gate_separates_invalid_records() -> None:
    valid = MatchRecord(date(2026, 8, 18), "A", "B", 1, 0)
    future = MatchRecord(date(2026, 8, 20), "C", "D", 0, 0)
    result = apply_quality_gate([valid, future], as_of=date(2026, 8, 19))
    assert result.accepted == (valid,)
    assert result.rejected == (future,)
    assert result.issues[0].code == "future_record"
