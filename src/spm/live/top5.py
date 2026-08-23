"""Generate the production Live Top 5 from upcoming fixtures."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.statistics.engine import SPMEngine, SPMScore
from spm.backtest.live_pipeline import run_live_pipeline
from spm.backtest.oos_ranking import OOSRankingEntry
from .scoring import score_fixtures


def build_upcoming_top5(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    as_of: date,
    engine: SPMEngine | None = None,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
) -> tuple:
    """Score upcoming fixtures and apply the canonical production Top-5 policy."""
    scores: tuple[SPMScore, ...] = score_fixtures(matches, fixtures, as_of=as_of, engine=engine)
    return run_live_pipeline(
        scores,
        oos_entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
