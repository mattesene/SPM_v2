from spm.backtest.oos_ranking import rank_oos_results
from spm.backtest.oos_staking import OOSStakingWindowResult


def test_roi_is_normalized_to_configured_initial_bankroll():
    first = OOSStakingWindowResult(None, 10, 10, 100.0, 1100.0, 20.0)
    second = OOSStakingWindowResult(None, 10, 10, 50.0, 1050.0, 10.0)
    ranked = rank_oos_results(
        [(first, "A"), (second, "B")],
        key_fn=lambda value: value,
        initial_bankroll=1000.0,
        min_bets=1,
    )
    assert ranked[0].roi == 0.10
    assert ranked[1].roi == 0.05


def test_min_bets_filter_is_applied_before_ranking():
    low_sample = OOSStakingWindowResult(None, 1, 2, 100.0, 1100.0, 0.0)
    enough_sample = OOSStakingWindowResult(None, 1, 10, 80.0, 1080.0, 0.0)
    ranked = rank_oos_results(
        [(low_sample, "low"), (enough_sample, "enough")],
        key_fn=lambda value: value,
        initial_bankroll=1000.0,
        min_bets=5,
    )
    assert [entry.key for entry in ranked] == ["enough"]
