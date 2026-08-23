"""Provider-agnostic acquisition layer for Live fixtures.

Providers implement fetch_fixtures(); this module deliberately contains no
network-specific code so provider credentials and scraping policies stay out
of the core model.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol, Sequence

from spm.data.fixtures import Fixture
from spm.data.repository import MatchRepository


class FixtureProvider(Protocol):
    def fetch_fixtures(self, from_date: date) -> Sequence[Fixture]: ...


@dataclass(frozen=True)
class AcquisitionResult:
    requested_from: date
    fixtures_seen: int
    fixtures_written: int


def acquire_fixtures(
    provider: FixtureProvider,
    repository: MatchRepository,
    *,
    from_date: date,
) -> AcquisitionResult:
    fixtures = list(provider.fetch_fixtures(from_date))
    written = 0
    for fixture in fixtures:
        repository.upsert_fixture(fixture)
        written += 1
    return AcquisitionResult(from_date, len(fixtures), written)
