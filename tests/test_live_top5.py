from spm.backtest.live_top5 import build_live_top5
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.statistics.engine import SPMScore


def _score(i: int) -> SPMScore:
    return SPMScore(f"H{i}", f"A{i}", .30, 30.0, .8, .8, .8, (.6, .15, .15, .1))


def test_build_live_top5_is_capped_and_filtered() -> None:
    scores = [_score(i) for i in range(7)]
    evidence = [OOSRankingEntry(f"H{i} vs A{i}", 20, 100.0 - i, .10, .80, 0, 0, 0) for i in range(7)]
    result = build_live_top5(scores, evidence)
    assert len(result) == 5
    assert result[0].fixture == ("H0", "A0")


def test_build_live_top5_rejects_weak_oos() -> None:
    result = build_live_top5(
        [_score(0)],
        [OOSRankingEntry("H0 vs A0", 19, 100.0, .10, .90, 0, 0, 0)],
    )
    assert result == ()
