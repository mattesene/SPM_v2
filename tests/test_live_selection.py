from datetime import date

from spm.backtest.live_selection import run_live_pipeline
from spm.statistics.engine import SPMScore


def score(home: str, away: str, value: float) -> SPMScore:
    return SPMScore(home, away, value / 100.0, value, .8, .8, .8, (.6, .15, .15, .1))


def test_live_selection_works_without_oos_ranking():
    result = run_live_pipeline([
        score("A", "B", 72),
        score("C", "D", 65),
    ], [])
    assert len(result) == 2
    assert result[0].fixture == ("A", "B")
    assert result[0].confidence == .72
    assert result[0].oos_score == 0


def test_live_selection_applies_oos_reliability_filter():
    from spm.backtest.oos_ranking import OOSRankingEntry

    result = run_live_pipeline(
        [score("A", "B", 72), score("C", "D", 80)],
        [
            OOSRankingEntry("A", 5, 40, 100, .1, 10, .75, .2),
            OOSRankingEntry("C", 5, 40, 100, .1, 10, .40, .2),
        ],
    )
    assert [item.fixture for item in result] == [("A", "B")]
