from spm.backtest.aggregation import TeamOOSStats
from spm.backtest.stability import rank_stability


def test_stability_rewards_repeated_presence():
    windows = [
        [TeamOOSStats("A", 30, 30, 24, .8), TeamOOSStats("B", 30, 30, 27, .9)],
        [TeamOOSStats("A", 30, 30, 24, .8)],
    ]
    result = rank_stability(windows, min_selections=20, top_n=5)
    assert result[0].team == "A"
    assert result[0].windows_present == 2


def test_empty_stability_is_empty():
    assert rank_stability([]) == ()
