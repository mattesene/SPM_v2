from datetime import date

from spm.data.models import Match
from spm.statistics.backtest import chronological_backtest


def test_chronological_backtest_never_uses_current_match() -> None:
    matches = [
        Match(date(2026, 7, 1), "A", "B", 1, 1),
        Match(date(2026, 7, 2), "A", "C", 1, 0),
        Match(date(2026, 7, 3), "B", "C", 0, 0),
        Match(date(2026, 7, 4), "A", "B", 2, 0),
    ]

    summary = chronological_backtest(matches)

    assert summary.skipped == 2
    assert summary.evaluated == 2
    assert summary.results[0].date == date(2026, 7, 3)
    assert summary.results[1].date == date(2026, 7, 4)
    assert all(0 <= item.draw_probability <= 1 for item in summary.results)


def test_backtest_summary_metrics() -> None:
    matches = [
        Match(date(2026, 7, 1), "A", "B", 1, 1),
        Match(date(2026, 7, 2), "A", "C", 1, 0),
        Match(date(2026, 7, 3), "B", "C", 0, 0),
        Match(date(2026, 7, 4), "A", "B", 2, 0),
        Match(date(2026, 7, 5), "C", "A", 1, 1),
    ]

    summary = chronological_backtest(matches)

    assert summary.evaluated == 3
    assert 0 <= summary.brier_score <= 1
    assert 0 <= summary.actual_draw_rate <= 1
