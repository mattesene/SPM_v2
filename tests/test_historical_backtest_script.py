from dataclasses import dataclass

from spm.statistics.backtest import BacktestSummary
from spm.statistics.backtest_runner import DatasetBacktest
from spm.statistics.competition_report import build_competition_report


@dataclass(frozen=True, slots=True)
class DummySummary:
    results: tuple = ()
    skipped: int = 2

    @property
    def evaluated(self):
        return 10

    @property
    def brier_score(self):
        return 0.2

    @property
    def actual_draw_rate(self):
        return 0.3


def test_competition_report_parses_seasoned_dataset_name():
    rows = build_competition_report((DatasetBacktest("E0_2025_26.csv", DummySummary()),))
    assert rows[0].competition == "E0"
    assert rows[0].season == "2025/26"
    assert rows[0].evaluated == 10
    assert rows[0].skipped == 2
