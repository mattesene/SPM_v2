"""Normalization helpers for externally acquired fixture data."""
from __future__ import annotations

from datetime import date
from dataclasses import dataclass

from spm.data.fixtures import Fixture


@dataclass(frozen=True)
class RawFixture:
    home: str
    away: str
    kickoff: date


def normalize_fixture(raw: RawFixture) -> Fixture:
    home = " ".join(raw.home.strip().split())
    away = " ".join(raw.away.strip().split())
    if not home or not away:
        raise ValueError("fixture teams cannot be empty")
    if home == away:
        raise ValueError("home and away teams must differ")
    return Fixture(home, away, raw.kickoff)


def normalize_fixtures(raw_fixtures: list[RawFixture]) -> list[Fixture]:
    return [normalize_fixture(item) for item in raw_fixtures]
