from datetime import date

from spm.backtest.engine import BacktestObservation
from spm.backtest.metrics import calculate_metrics


def test_calculate_metrics_reports_selection_and_hits():
    observations = [
        BacktestObservation(date(2025, 1, 1), "A", "B", 0.60, 1, True),
        BacktestObservation(date(2025, 1, 2), "B", "C", 0.55, 0, True),
        BacktestObservation(date(2025, 1, 3), "C", "A", 0.40, 1, False),
    ]
    metrics = calculate_metrics(observations)
    assert metrics.observations == 3
    assert metrics.selected == 2
    assert metrics.draws == 2
    assert metrics.selected_draws == 1
    assert metrics.selection_rate == 2 / 3
    assert metrics.hit_rate == 0.5
    assert metrics.draw_rate == 2 / 3
