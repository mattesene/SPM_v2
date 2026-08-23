from dataclasses import SimpleNamespace

from spm.backtest.oos_bridge import build_oos_entries


def test_build_oos_entries_aggregates_by_key() -> None:
    first = SimpleNamespace(bets=4, profit=30.0, max_drawdown=10.0)
    second = SimpleNamespace(bets=6, profit=-5.0, max_drawdown=20.0)
    rows = [(first, "A"), (second, "A")]
    result = build_oos_entries(rows, key_fn=lambda value: value, min_bets=1)
    assert len(result) == 1
    assert result[0].key == "A"
    assert result[0].bets == 10
    assert result[0].profit == 25.0
    assert result[0].max_drawdown == 20.0
    assert result[0].windows == 2
