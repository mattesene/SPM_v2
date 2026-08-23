from spm.backtest.live_pipeline import run_live_pipeline
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.statistics.engine import SPMScore


def test_live_pipeline_reaches_top5_from_spm_and_oos() -> None:
    scores = [
        SPMScore(f"H{i}", f"A{i}", .30 + i * .001, 30.0 - i, .8, .8, .8, (.6, .15, .15, .1))
        for i in range(6)
    ]
    evidence = [
        OOSRankingEntry(f"H{i} vs A{i}", 20, 100.0 - i, .10, .80, 0, 0, 0)
        for i in range(6)
    ]
    result = run_live_pipeline(scores, evidence)
    assert len(result) == 5
    assert all(item.bets >= 20 for item in result)
    assert all(item.profitable_window_rate >= .50 for item in result)
    assert all(item.combined_score >= 0 for item in result)
    assert all(0 <= item.confidence <= 1 for item in result)
