from datetime import date

from spm.data.fixtures import Fixture
from spm.live.quality import quality_gate


def test_quality_gate_removes_duplicates_and_rejects_invalid():
    fixtures = [
        Fixture("A", "B", date(2026, 8, 24)),
        Fixture("A", "B", date(2026, 8, 24)),
        Fixture("", "C", date(2026, 8, 24)),
        Fixture("D", "D", date(2026, 8, 25)),
    ]
    result = quality_gate(fixtures)
    assert len(result.accepted) == 1
    assert result.duplicates_removed == 1
    assert result.rejected == 2
