from datetime import date

from spm.backtest.engine import BacktestObservation
from spm.backtest.selection_metrics import summarize_selection


def test_selection_metrics_distinguish_all_and_selected_rows():
    rows = (
        BacktestObservation(date(2025, 1, 1), "A", "B", 0.6, 1, True),
        BacktestObservation(date(2025, 1, 2), "B", "C", 0.4, 0, True),
        BacktestObservation(date(2025, 1, 3), "C", "A", 0.3, 1, False),
    )
    metrics = summarize_selection(rows)
    assert metrics.observations == 3
    assert metrics.selected == 2
    assert metrics.draws == 2
    assert metrics.selected_draws == 1
    assert metrics.draw_rate == 2 / 3
    assert metrics.selected_draw_rate == 0.5
