"""Run leakage-safe backtests independently for each competition slice."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from spm.backtest.engine import BacktestObservation, ChronologicalBacktester
from spm.data.models import Match
from spm.data.normalized import MatchRecord
from spm.ingestion.backtest_input import to_backtest_matches
from spm.ingestion.validation import validate_historical_dataset


def run_by_competition(
    records: Iterable[MatchRecord],
    *,
    min_history: int = 3,
    threshold: float = 0.0,
) -> dict[str, tuple[BacktestObservation, ...]]:
    """Validate records and backtest each competition independently."""
    groups: defaultdict[str, list[MatchRecord]] = defaultdict(list)
    for record in validate_historical_dataset(records):
        groups[record.competition or "unknown"].append(record)

    return {
        competition: ChronologicalBacktester(
            min_history=min_history,
            threshold=threshold,
        ).run(to_backtest_matches(group))
        for competition, group in sorted(groups.items())
    }
