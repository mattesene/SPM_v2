"""Run leakage-safe backtests independently for each competition slice."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from spm.backtest.engine import BacktestObservation, ChronologicalBacktester
from spm.data.models import Match


def run_by_competition(
    matches: Iterable[Match],
    *,
    min_history: int = 3,
    threshold: float = 0.0,
) -> dict[str, tuple[BacktestObservation, ...]]:
    """Backtest each competition independently and return keyed observations."""
    groups: defaultdict[str, list[Match]] = defaultdict(list)
    for match in matches:
        competition = getattr(match, "competition", None) or "unknown"
        groups[competition].append(match)
    return {
        competition: ChronologicalBacktester(min_history=min_history, threshold=threshold).run(group)
        for competition, group in sorted(groups.items())
    }
