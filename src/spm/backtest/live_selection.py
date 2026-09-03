"""Production live candidate selection joining SPM scores and OOS evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .oos_ranking import OOSRankingEntry
from spm.statistics.engine import SPMScore


@dataclass(frozen=True, slots=True)
class LiveCandidate:
    fixture: tuple[str, str]
    confidence: float
    combined_score: float
    spm_score: float
    oos_score: float
    bets: int
    profitable_window_rate: float
    selected_team: str = ""
    team_probability: float = 0.0
    team_streak: int = 0
    streak_draw_rate: float = 0.0


def _oos_for_fixture(home: str, away: str, entries: dict[str, OOSRankingEntry]) -> OOSRankingEntry | None:
    keys = (f"{home}|{away}", f"{home} vs {away}", home, away)
    for key in keys:
        if key in entries:
            return entries[key]
    return None


def run_live_pipeline(
    scores: Iterable[SPMScore],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
) -> tuple[LiveCandidate, ...]:
    """Return the production Top-5 team selections, not merely top fixtures."""
    if not 0 <= oos_weight <= 1:
        raise ValueError("oos_weight must be between 0 and 1")
    oos = {entry.key: entry for entry in oos_entries}
    has_oos = bool(oos)
    candidates: list[LiveCandidate] = []
    for score in scores:
        entry = _oos_for_fixture(score.home_team, score.away_team, oos)
        if has_oos:
            if entry is None:
                continue
            if entry.bets < min_bets or entry.profitable_window_rate < min_profitable_window_rate:
                continue
            oos_component = max(0.0, min(100.0, entry.score * 100.0))
            combined = score.spm_score * (1.0 - oos_weight) + oos_component * oos_weight
            bets = entry.bets
            rate = entry.profitable_window_rate
            oos_score = oos_component
        else:
            combined = score.spm_score
            bets = 0
            rate = 0.0
            oos_score = 0.0
        candidates.append(
            LiveCandidate(
                fixture=(score.home_team, score.away_team),
                confidence=max(0.0, min(1.0, combined / 100.0)),
                combined_score=combined,
                spm_score=score.spm_score,
                oos_score=oos_score,
                bets=bets,
                profitable_window_rate=rate,
                selected_team=score.selected_team,
                team_probability=score.team_probability,
                team_streak=score.selected_team_streak,
                streak_draw_rate=score.selected_team_streak_draw_rate,
            )
        )
    return tuple(sorted(candidates, key=lambda item: (-item.team_probability, -item.combined_score, -item.team_streak, item.selected_team)))[:5]
