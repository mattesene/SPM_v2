"""Combine today's SPM score with validated OOS evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from spm.statistics.engine import SPMScore
from .oos_ranking import OOSRankingEntry


@dataclass(frozen=True, slots=True)
class LiveCandidate:
    fixture: tuple[str, str]
    spm_score: float
    oos_score: float
    profitable_window_rate: float
    bets: int
    combined_score: float
    confidence: float


def select_live_candidates(
    scores: Iterable[SPMScore],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
    limit: int = 5,
) -> tuple[LiveCandidate, ...]:
    if min_bets < 0 or not 0 <= min_profitable_window_rate <= 1:
        raise ValueError("invalid OOS thresholds")
    if not 0 <= oos_weight <= 1 or limit < 1:
        raise ValueError("invalid weighting or limit")
    evidence = {
        entry.key: entry
        for entry in oos_entries
        if entry.bets >= min_bets and entry.profitable_window_rate >= min_profitable_window_rate
    }
    candidates: list[LiveCandidate] = []
    for score in scores:
        key = f"{score.home_team} vs {score.away_team}"
        entry = evidence.get(key)
        if entry is None:
            continue
        combined = (1.0 - oos_weight) * score.spm_score + oos_weight * entry.score
        confidence = (
            0.35 * score.draw_probability
            + 0.25 * score.draw_signal
            + 0.20 * score.form_balance
            + 0.20 * entry.profitable_window_rate
        )
        candidates.append(LiveCandidate(
            (score.home_team, score.away_team), score.spm_score, entry.score,
            entry.profitable_window_rate, entry.bets, combined, confidence,
        ))
    candidates.sort(key=lambda item: (-item.combined_score, -item.confidence, item.fixture))
    return tuple(candidates[:limit])
