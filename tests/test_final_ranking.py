from spm.backtest.aggregation import TeamOOSStats
from spm.backtest.final_ranking import final_top_teams


def test_final_ranking_is_numbered_and_stable():
    windows = [
        [TeamOOSStats("A", 30, 30, 24, .8), TeamOOSStats("B", 30, 30, 27, .9)],
        [TeamOOSStats("A", 30, 30, 24, .8), TeamOOSStats("C", 30, 30, 26, .867)],
    ]
    result = final_top_teams(windows, min_selections=20, top_n=3)
    assert result[0].rank == 1
    assert result[0].team == "A"
    assert result[0].windows_present == 2
