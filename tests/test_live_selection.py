from spm.backtest.live_selection import select_live_candidates
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.statistics.engine import SPMScore


def test_live_selection_requires_oos_evidence() -> None:
    score = SPMScore("A", "B", 0.32, 32.0, 0.8, 0.8, 0.8, (0.6, 0.15, 0.15, 0.1))
    evidence = OOSRankingEntry("A vs B", 20, 100.0, 0.10, 0.80, 0.0, 0.0, 0.0)
    result = select_live_candidates([score], [evidence], min_bets=20, min_profitable_window_rate=0.50)
    assert len(result) == 1
    assert result[0].fixture == ("A", "B")
    assert result[0].combined_score == 40.12
    assert result[0].confidence == 0.548


def test_live_selection_excludes_insufficient_evidence() -> None:
    score = SPMScore("A", "B", 0.32, 32.0, 0.8, 0.8, 0.8, (0.6, 0.15, 0.15, 0.1))
    evidence = OOSRankingEntry("A vs B", 19, 100.0, 0.10, 0.90, 0.0, 0.0, 0.0)
    assert select_live_candidates([score], [evidence]) == ()
