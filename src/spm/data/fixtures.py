"""Upcoming fixture domain model."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class Fixture:
    """A scheduled football fixture without a final result."""

    home_team: str
    away_team: str
    date: date

    def __post_init__(self) -> None:
        if not self.home_team.strip() or not self.away_team.strip():
            raise ValueError("Team names cannot be empty")
