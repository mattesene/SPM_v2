from spm.backtest.oos_ranking import OOSRankingEntry
from spm.backtest.stability_report import add_stability


def test_stability_is_attached_to_ranking():
    row = OOSRankingEntry("A", 20, 50, 100, .10, 10, .75, .1)
    result = add_stability([row])
    assert len(result) == 1
    assert result[0].stability.trials == 20
    assert result[0].stability.success_rate == .75


def test_stability_threshold_can_mark_entry_robust():
    row = OOSRankingEntry("A", 100, 100, 100, .10, 0, .70, .1)
    result = add_stability([row], min_lower_95=.60)
    assert result[0].robust is True
