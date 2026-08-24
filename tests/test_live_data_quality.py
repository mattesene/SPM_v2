from datetime import date, timedelta

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.live.data_quality import assess_live_data


def test_quality_accepts_fresh_unique_data():
    as_of = date(2026, 8, 24)
    matches = [Match(as_of - timedelta(days=2), "A", "B", 1, 1)]
    fixtures = [Fixture("C", "D", as_of)]
    report = assess_live_data(matches, fixtures, as_of=as_of)
    assert report.ok
    assert report.warnings == ()


def test_quality_detects_duplicates_and_stale_data():
    as_of = date(2026, 8, 24)
    old = Match(as_of - timedelta(days=30), "A", "B", 1, 0)
    report = assess_live_data([old, old], [], as_of=as_of)
    assert report.duplicate_matches == 1
    assert report.stale_match_data
    assert not report.ok
    assert len(report.warnings) == 2
