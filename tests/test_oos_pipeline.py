from spm.backtest.oos_pipeline import run_oos_odds_pipeline


def test_oos_pipeline_returns_top_candidates_from_real_staking_results():
    datasets = [
        ("A", [("A", True, 3.0)] * 5),
        ("B", [("B", False, 2.0)] * 5),
    ]
    result = run_oos_odds_pipeline(
        datasets,
        initial_bankroll=1000.0,
        base_stake=10.0,
        min_bets=5,
        limit=5,
    )
    assert result
    assert result[0].key == "A"
    assert result[0].bets == 5


def test_oos_pipeline_respects_top_n_limit():
    datasets = [
        (str(i), [(str(i), True, 2.0)] * 5) for i in range(8)
    ]
    result = run_oos_odds_pipeline(
        datasets,
        initial_bankroll=1000.0,
        base_stake=10.0,
        min_bets=5,
        limit=3,
    )
    assert len(result) == 3
