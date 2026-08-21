"""Build dashboard snapshots from canonical SPM ranking results."""
from __future__ import annotations

from datetime import date

from spm.statistics.engine import RankingResult
from spm.ui.contracts import DashboardSnapshot, FixtureCard


def snapshot_from_ranked(
    ranked: list[RankingResult],
    *,
    as_of: date,
    bankroll: float = 0.0,
    profit: float = 0.0,
    drawdown: float = 0.0,
) -> DashboardSnapshot:
    cards = tuple(
        FixtureCard(
            home_team=item.home_team,
            away_team=item.away_team,
            spm_score=item.spm_score,
            draw_probability=item.draw_probability,
        )
        for item in ranked
    )
    return DashboardSnapshot(
        as_of=as_of,
        bankroll=bankroll,
        profit=profit,
        drawdown=drawdown,
        selections=cards,
    )
