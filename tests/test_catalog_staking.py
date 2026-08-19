from spm.backtest.catalog_staking import run_catalog_staking


def test_catalog_staking_flattens_datasets_deterministically():
    result = run_catalog_staking({"b": [False, True], "a": [True]})
    assert result.datasets == 2
    assert result.observations == 3
    assert result.draw_rate == 2 / 3
    assert result.staking.bets == 3
