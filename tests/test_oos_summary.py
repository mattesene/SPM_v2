from spm.backtest.oos_ranking import OOSRankingEntry
from spm.backtest.oos_summary import summarize_oos


def test_summarize_oos() -> None:
    rows = (
        OOSRankingEntry("A", 2, 10, 120.0, 0.12, 30.0, 0.5, 0.20),
        OOSRankingEntry("B", 1, 5, -20.0, -0.02, 15.0, 0.0, -0.03),
    )
    result = summarize_oos(rows)
    assert result.entities == 2
    assert result.eligible_entities == 2
    assert result.total_bets == 15
    assert result.total_profit == 100.0
    assert result.best_key == "A"
