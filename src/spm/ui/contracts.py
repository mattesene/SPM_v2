"""Stable, framework-neutral data contracts for the SPM_v2 UI."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class FixtureCard:
    home_team: str
    away_team: str
    spm_score: float
    draw_probability: float
    draw_odds: float | None = None
    implied_probability: float | None = None
    edge: float | None = None
    streak: int = 0


@dataclass(frozen=True)
class ProgressionCard:
    team: str
    level: int
    current_stake: float
    exposure: float
    active: bool = True


@dataclass(frozen=True)
class DashboardSnapshot:
    as_of: date
    bankroll: float
    profit: float
    drawdown: float
    selections: tuple[FixtureCard, ...] = field(default_factory=tuple)
    progressions: tuple[ProgressionCard, ...] = field(default_factory=tuple)
