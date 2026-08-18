from spm.backtest.staking_report import run_staking_backtest


def test_staking_report_tracks_rate_and_observations():
    report = run_staking_backtest([False, True, True])
    assert report.observations == 3
    assert report.draw_rate == 2 / 3
    assert report.staking.wins == 2
