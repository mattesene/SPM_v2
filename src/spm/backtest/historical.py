"""Historical backtest orchestration over chronologically ordered matches."""
from __future__ import annotations

from spm.data.models import Match

from .engine import ChronologicalBacktester
from .report import BacktestReport


def run_historical_backtest(
    matches: list[Match],
    min_history: int = 1,
    threshold: float = 0.5,
) -> BacktestReport:
    """Run a chronological, leakage-safe backtest and build its report."""
    observations = ChronologicalBacktester(
        min_history=min_history,
        threshold=threshold,
    ).run(matches)
    actual = ["D" if observation.actual_draw else "N" for observation in observations]
    predicted = ["D" if observation.selected else "N" for observation in observations]
    probabilities = [observation.probability for observation in observations]
    outcomes = [observation.actual_draw for observation in observations]
    return BacktestReport.from_predictions(actual, predicted, probabilities, outcomes)
