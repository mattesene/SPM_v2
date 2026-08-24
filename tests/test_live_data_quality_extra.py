from datetime import date

from spm.data.fixtures import Fixture
from spm.live.data_quality import assess_live_data


def test_quality_reports_duplicate_upcoming_fixture():
    day = date(2026, 8, 25)
    fixture = Fixture("A", "B", day)
    report = assess_live_data([], [fixture, fixture], as_of=date(2026, 8, 24))
    assert report.duplicate_fixtures == 1
    assert not report.ok


def test_quality_uses_whitespace_normalized_fixture_keys():
    day = date(2026, 8, 25)
    a = Fixture(" A ", "B", day)
    b = Fixture("A", "B", day)
    report = assess_live_data([], [a, b], as_of=date(2026, 8, 24))
    assert report.duplicate_fixtures == 1
