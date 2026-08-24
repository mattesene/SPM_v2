"""Quality gates for production Live match and fixture data."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.data.models import Match


@dataclass(frozen=True, slots=True)
class DataQualityReport:
    match_count: int
    fixture_count: int
    duplicate_matches: int
    duplicate_fixtures: int
    invalid_fixtures: int
    stale_match_data: bool
    warnings: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.duplicate_matches and not self.duplicate_fixtures and not self.invalid_fixtures and not self.stale_match_data


def assess_live_data(matches: Iterable[Match], fixtures: Iterable[Fixture], *, as_of: date, max_match_age_days: int = 14) -> DataQualityReport:
    """Assess persisted Live inputs without modifying them."""
    match_rows = tuple(matches)
    fixture_rows = tuple(fixtures)
    match_keys = [(m.date, m.home_team.strip(), m.away_team.strip()) for m in match_rows]
    fixture_keys = [(f.date, f.home_team.strip(), f.away_team.strip()) for f in fixture_rows]
    duplicate_matches = len(match_keys) - len(set(match_keys))
    duplicate_fixtures = len(fixture_keys) - len(set(fixture_keys))
    invalid_fixtures = sum(1 for f in fixture_rows if f.home_team.strip() == f.away_team.strip())
    latest_match = max((m.date for m in match_rows), default=None)
    stale = latest_match is None or latest_match < as_of - timedelta(days=max_match_age_days)
    warnings: list[str] = []
    if duplicate_matches:
        warnings.append(f"duplicate completed matches: {duplicate_matches}")
    if duplicate_fixtures:
        warnings.append(f"duplicate upcoming fixtures: {duplicate_fixtures}")
    if invalid_fixtures:
        warnings.append(f"invalid fixtures: {invalid_fixtures}")
    if stale:
        warnings.append("completed match data is stale or missing")
    return DataQualityReport(len(match_rows), len(fixture_rows), duplicate_matches, duplicate_fixtures, invalid_fixtures, stale, tuple(warnings))
