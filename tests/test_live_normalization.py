from datetime import date

import pytest

from spm.live.normalization import RawFixture, normalize_fixture


def test_normalize_fixture_cleans_team_names():
    fixture = normalize_fixture(RawFixture("  Team   A ", "Team B  ", date(2026, 8, 24)))
    assert fixture.home == "Team A"
    assert fixture.away == "Team B"


def test_normalize_fixture_rejects_empty_team():
    with pytest.raises(ValueError):
        normalize_fixture(RawFixture("", "Team B", date(2026, 8, 24)))


def test_normalize_fixture_rejects_same_team():
    with pytest.raises(ValueError):
        normalize_fixture(RawFixture("Team A", "Team A", date(2026, 8, 24)))
