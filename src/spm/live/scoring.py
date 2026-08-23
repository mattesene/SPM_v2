"""Build SPM scores for persisted upcoming fixtures."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.statistics.engine import SPMEngine, SPMScore


def score_fixtures(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    *,
    as_of: date,
    engine: SPMEngine | None = None,
) -> tuple[SPMScore, ...]:
    """Score only fixtures scheduled on/after the analysis date."""
    scorer = engine or SPMEngine()
    upcoming = sorted((fixture for fixture in fixtures if fixture.date >= as_of), key=lambda item: item.date)
    return tuple(
        scorer.score(matches, fixture.home_team, fixture.away_team, as_of)
        for fixture in upcoming
    )
