from datetime import date

from spm.backtest.market_report import build_market_group_report, group_by_season, group_by_team, staking_summary
from spm.backtest.market_runner import MarketBacktestObservation
from spm.backtest.odds_staking import OddsStakingResult


def rows():
    return (
        MarketBacktestObservation(date(2025, 1, 1), "A", "B", .4, False, True, 3.0),
        MarketBacktestObservation(date(2025, 2, 1), "A", "C", .5, True, True, 3.2),
        MarketBacktestObservation(date(2026, 1, 1), "D", "E", .3, True, False, None),
    )


def test_group_report_is_deterministic():
    report = build_market_group_report(rows(), key_fn=group_by_season)
    assert [item.key for item in report] == ["2025", "2026"]
    assert report[0].selected == 2
    assert report[0].priced == 2
    assert report[0].priced_draw_rate == .5


def test_team_group_report():
    report = build_market_group_report(rows(), key_fn=group_by_team)
    assert [item.key for item in report] == ["A", "D"]


def test_staking_summary():
    result = OddsStakingResult(110.0, 10.0, 20.0, 30.0, 4, 2, 1)
    summary = staking_summary(result)
    assert summary["profit"] == 10.0
    assert summary["win_rate"] == .5
    assert summary["roi_on_max_exposure"] == 10 / 30
