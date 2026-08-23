"""End-to-end fixture acquisition pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.repository import MatchRepository
from spm.data.fixtures import Fixture
from spm.live.acquisition import FixtureProvider
from spm.live.normalization import RawFixture, normalize_fixtures
from spm.live.quality import quality_gate


@dataclass(frozen=True)
class PipelineResult:
    fetched: int
    written: int
    rejected: int
    duplicates_removed: int


def acquire_and_normalize(provider: FixtureProvider, repository: MatchRepository, *, from_date: date) -> PipelineResult:
    raw = list(provider.fetch_fixtures(from_date))
    raw_fixtures = [item for item in raw if isinstance(item, RawFixture)]
    direct = [item for item in raw if isinstance(item, Fixture)]
    fixtures = normalize_fixtures(raw_fixtures) + direct
    quality = quality_gate(fixtures)
    for fixture in quality.accepted:
        repository.upsert_fixture(fixture)
    if quality.accepted:
        repository.mark_fixtures_refreshed()
    return PipelineResult(
        fetched=len(raw),
        written=len(quality.accepted),
        rejected=quality.rejected,
        duplicates_removed=quality.duplicates_removed,
    )
