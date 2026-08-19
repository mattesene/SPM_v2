from spm.backtest.team_staking import run_team_staking


def test_team_staking_keeps_sequences_independent():
    report = run_team_staking({"A": [False, True], "B": [True]})
    assert report.teams == 2
    assert report.selected == 2
    assert report.staking.bets == 3
    assert report.staking.wins == 2
