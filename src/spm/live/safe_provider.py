"""Failure-safe wrapper for Live fixture providers."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Sequence

from spm.data.fixtures import Fixture
from spm.live.acquisition import FixtureProvider


@dataclass(frozen=True)
class ProviderResult:
    fixtures: Sequence[Fixture]
    source_ok: bool
    error: str | None = None


def safe_fetch(provider: FixtureProvider, from_date: date) -> ProviderResult:
    try:
        return ProviderResult(provider.fetch_fixtures(from_date), True)
    except Exception as exc:  # provider failures must not crash the scheduler
        return ProviderResult([], False, f"{type(exc).__name__}: {exc}")
