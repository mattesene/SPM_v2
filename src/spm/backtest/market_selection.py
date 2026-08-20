"""Market-aware SPM selection rules."""
from __future__ import annotations

from spm.model.signal import SPMSignal, build_signal


def select_market_signal(
    team: str,
    streak: int,
    probability: float,
    draw_odds: float | None,
    *,
    min_streak: int = 0,
    min_edge: float = 0.0,
) -> SPMSignal | None:
    """Return a signal only when a usable draw price exists and thresholds pass."""
    if draw_odds is None:
        return None
    return build_signal(
        team,
        streak,
        probability,
        draw_odds,
        min_streak=min_streak,
        min_edge=min_edge,
    )
