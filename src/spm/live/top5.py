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
    """Score upcoming fixtures and apply the existing production Top-5 policy."""
    scores = score_upcoming_fixtures(matches, fixtures, as_of=as_of, engine=engine)
    entries = tuple(oos_entries)
    candidates = run_live_pipeline(
        scores,
        entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
    print(f"live_top5,fixtures_scored={len(scores)},oos_entries={len(entries)},candidates={len(candidates)}")

    # SPM-only mode must never publish an empty dashboard when scored fixtures
    # exist. This is the same policy as run_live_pipeline, kept here as a
    # defensive guard for the production reporting path.
    if not entries and scores and not candidates:
        fallback = tuple(
            LiveCandidate(
                fixture=(score.home_team, score.away_team),
                confidence=max(0.0, min(1.0, score.spm_score / 100.0)),
                combined_score=score.spm_score,
                spm_score=score.spm_score,
                oos_score=0.0,
                bets=0,
                profitable_window_rate=0.0,
            )
            for score in sorted(scores, key=lambda item: (-item.spm_score, item.home_team, item.away_team))[:5]
        )
        print(f"live_top5,fallback_spm_only={len(fallback)}")
        return fallback

    return candidates
