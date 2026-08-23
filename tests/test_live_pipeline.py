from spm.backtest.live_pipeline import build_live_top5
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.statistics.engine import SPMScore


def test_live_pipeline_is_capped_at_five() -> None:
    scores = [SPMScore(f"H{i}", f"A{i}", .30, 30.0, .8, .8, .8, (.6, .15, .15, .1)) for i in range(7)]
    evidence = [OOSRankingEntry(f"H{i} vs A{i}", 2, 20, 100.0, .1, .0, .8, 1.0) for i in range(7)]
    result = build_live_top5(scores, evidence, min_bets=20)
    assert len(result) == 5
