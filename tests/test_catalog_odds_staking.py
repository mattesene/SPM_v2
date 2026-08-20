import pytest

from spm.backtest.catalog_staking import run_catalog_odds_staking


def test_catalog_odds_staking_uses_match_specific_prices():
    result = run_catalog_odds_staking(
        {
            "B": [(True, 3.0)],
            "A": [(False, 3.0), (True, 3.5)],
        },
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.datasets == 2
    assert result.observations == 3
    assert result.selected == 3
    assert result.draw_rate == pytest.approx(2 / 3)
    assert result.staking.final_bankroll == pytest.approx(160.0)


def test_catalog_odds_staking_counts_missing_prices_as_unselected():
    result = run_catalog_odds_staking(
        {"A": [(False, None), (True, 3.0)]},
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.observations == 2
    assert result.selected == 1
    assert result.staking.skipped == 1
