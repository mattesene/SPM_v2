"""Production-facing Top-5 draw opportunity selection."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .engine import SPMScore


@dataclass(frozen=True, slots=True)
class Top5Candidate:
    rank: int
    score: SPMScore
    confidence: float
    eligible: bool


def select_top5(scores: Iterable[SPMScore], *, min_probability: float = 0.20, min_confidence: float = 0.50) -> tuple[Top5Candidate, ...]:
    """Return at most five candidates, requiring both probability and signal agreement."""
    if not 0 <= min_probability <= 1 or not 0 <= min_confidence <= 1:
        raise ValueError("thresholds must be between 0 and 1")
    ranked = sorted(scores, key=lambda item: (-item.spm_score, item.home_team, item.away_team))
    output: list[Top5Candidate] = []
    for item in ranked:
        confidence = (item.form_balance + item.draw_signal + item.goal_balance_signal) / 3.0
        eligible = item.draw_probability >= min_probability and confidence >= min_confidence
        if eligible:
            output.append(Top5Candidate(len(output) + 1, item, confidence, True))
        if len(output) == 5:
            break
    return tuple(output)
