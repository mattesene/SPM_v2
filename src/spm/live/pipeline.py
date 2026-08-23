"""End-to-end fixture acquisition pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.repository import MatchRepository
from spm.live.acquisition import FixtureProvider
from spm.live.normalization import RawFixture, normalize_fixtures


@dataclass(frozen=True)
class PipelineResult:
    fetched: int
    written: int


def acquire_and_normalize(provider: FixtureProvider, repository: MatchRepository, *, from_date: date) -> PipelineResult:
    raw = list(provider.fetch_fixtures(from_date))
    # Providers may return Fixture instances directly or RawFixture records.
    normalized = normalize_fixtures([item for item in raw if isinstance(item, RawFixture)])
    direct = [item for item in raw if not isinstance(item, RawFixture)]
    fixtures = normalized + direct
    for fixture in fixtures:
        repository.upsert_fixture(fixture)
    return PipelineResult(len(raw), len(fixtures))
