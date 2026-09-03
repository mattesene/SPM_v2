"""Generate the production Live Top 5 from upcoming fixtures."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.statistics.engine import SPMEngine, SPMScore
from spm.backtest.live_selection import LiveCandidate, run_live_pipeline
from spm.backtest.oos_ranking import OOSRankingEntry
from .scoring import score_fixtures


def score_upcoming_fixtures(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    *,
    as_of: date,
    engine: SPMEngine | None = None,
) -> tuple[SPMScore, ...]:
    """Expose the canonical SPM scoring stage without applying Top-5 policy."""
    return score_fixtures(matches, fixtures, as_of=as_of, engine=engine)


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
) -> tuple[LiveCandidate, ...]:
    """Rank the five strongest teams for a draw series."""
    scores = score_upcoming_fixtures(matches, fixtures, as_of=as_of, engine=engine)
    entries = tuple(oos_entries)
    candidates = run_live_pipeline(
        scores,
        entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
    print(f"live_top5,teams_ranked={len(scores)},oos_entries={len(entries)},candidates={len(candidates)}")

    if not entries and scores and not candidates:
        fallback = tuple(
            LiveCandidate(
                fixture=(score.home_team, score.away_team),
                confidence=max(0.0, min(1.0, score.team_probability)),
                combined_score=score.team_probability * 100.0,
                spm_score=score.spm_score,
                oos_score=0.0,
                bets=0,
                profitable_window_rate=0.0,
                selected_team=score.selected_team,
                team_probability=score.team_probability,
                team_streak=score.selected_team_streak,
                streak_draw_rate=score.selected_team_streak_draw_rate,
            )
            for score in sorted(
                scores,
                key=lambda item: (-item.team_probability, -item.selected_team_streak, item.selected_team),
            )[:5]
        )
        print(f"live_top5,fallback_spm_only={len(fallback)}")
        return fallback

    return candidates
