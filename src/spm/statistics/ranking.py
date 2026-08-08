"""Fixture ranking by estimated draw probability."""

from dataclasses import dataclass
from collections.abc import Iterable

from spm.data.season import Season
from .model import PareggioModel


@dataclass(frozen=True, slots=True)
class Fixture:
    home_team: str
    away_team: str


@dataclass(frozen=True, slots=True)
class RankedFixture:
    fixture: Fixture
    probability: float


def rank_draws(season: Season, fixtures: Iterable[Fixture], model: PareggioModel | None = None) -> list[RankedFixture]:
    estimator = model or PareggioModel()
    ranked = []
    for fixture in fixtures:
        prediction = estimator.predict(season, fixture.home_team, fixture.away_team)
        ranked.append(RankedFixture(fixture, prediction.probability))
    return sorted(ranked, key=lambda item: item.probability, reverse=True)
