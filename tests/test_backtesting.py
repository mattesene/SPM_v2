from datetime import date, timedelta

from spm.data.models import Match
from spm.statistics.backtesting import Backtester


def make_history() -> list[Match]:
    base = date(2026, 1, 1)
    teams = [("A", "B"), ("B", "C"), ("C", "A")]
    scores = [(1, 1), (2, 0), (0, 1), (1, 0), (0, 0), (2, 1), (1, 1), (0, 0), (1, 2), (1, 1), (2, 0), (0, 0)]
    return [Match(base + timedelta(days=i), *teams[i % 3], *scores[i]) for i in range(len(scores))]


def test_backtester_is_chronological_and_returns_metrics() -> None:
    report = Backtester().run(make_history(), min_history=3)
    assert report.predictions
    assert 0 <= report.accuracy <= 1
    assert 0 <= report.precision <= 1
    assert 0 <= report.recall <= 1
    assert 0 <= report.f1 <= 1
    assert 0 <= report.brier_score <= 1
    assert 0 <= report.baseline_brier_score <= 1
