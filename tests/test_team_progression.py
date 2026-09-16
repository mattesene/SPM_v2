from datetime import date

from spm.backtest.team_progression import run_team_progression_backtest
from spm.data.models import Match


def _match(day: int, home: str, away: str, result: str) -> Match:
    home_goals, away_goals = {
        "D": (1, 1),
        "H": (2, 0),
        "A": (0, 2),
    }[result]
    return Match(
        date=date(2025, 1, day),
        home_team=home,
        away_team=away,
        home_goals=home_goals,
        away_goals=away_goals,
    )


def test_progression_doubles_stake_after_non_draw():
    matches = [
        _match(1, "A", "B", "H"),
        _match(2, "A", "C", "H"),
        _match(3, "A", "D", "H"),
        _match(4, "A", "E", "H"),
        _match(5, "A", "F", "H"),
        _match(6, "A", "G", "H"),
        _match(7, "A", "H", "D"),
    ]

    report = run_team_progression_backtest(matches, min_history=5, top_n=1)

    assert report.bets >= 1
    assert report.max_stake_units == 2
    assert report.max_capital_units == 3


def test_two_active_progressions_settle_on_same_fixture():
    matches = [
        _match(1, "A", "X", "H"),
        _match(2, "A", "Y", "H"),
        _match(3, "A", "Z", "H"),
        _match(4, "A", "W", "H"),
        _match(5, "A", "V", "H"),
        _match(1, "B", "Q", "H"),
        _match(2, "B", "R", "H"),
        _match(3, "B", "S", "H"),
        _match(4, "B", "T", "H"),
        _match(5, "B", "U", "H"),
        _match(6, "A", "C", "H"),
        _match(6, "B", "D", "H"),
        _match(7, "A", "B", "D"),
    ]

    report = run_team_progression_backtest(
        matches, min_history=5, top_n=2, draw_odds=3.0
    )

    # A and B are selected independently on day 6, both lose, then both
    # stake 2 units on the day-7 A-B fixture and both win.
    assert report.bets == 4
    assert report.max_stake_units == 2
    assert report.max_capital_units == 6
    assert report.total_staked_units == 6.0
    assert report.profit_units == 6.0
    assert report.max_drawdown_units == 2.0


def test_odds_economics_are_explicit_and_exact():
    matches = [
        _match(1, "A", "B", "H"),
        _match(2, "A", "C", "H"),
        _match(3, "A", "D", "H"),
        _match(4, "A", "E", "H"),
        _match(5, "A", "F", "H"),
        _match(6, "A", "G", "H"),
        _match(7, "A", "H", "H"),
        _match(8, "A", "I", "D"),
    ]

    report = run_team_progression_backtest(
        matches, min_history=5, top_n=1, draw_odds=3.0
    )

    assert report.profit_units == 3.0
    assert report.total_staked_units == 3.0
    assert report.roi == 1.0
    assert report.max_drawdown_units == 1.0
    assert report.draw_odds == 3.0


def test_odds_below_two_can_leave_a_completed_series_in_loss():
    matches = [
        _match(1, "A", "B", "H"),
        _match(2, "A", "C", "H"),
        _match(3, "A", "D", "H"),
        _match(4, "A", "E", "H"),
        _match(5, "A", "F", "H"),
        _match(6, "A", "G", "H"),
        _match(7, "A", "H", "H"),
        _match(8, "A", "I", "D"),
    ]

    report = run_team_progression_backtest(
        matches, min_history=5, top_n=1, draw_odds=1.4
    )

    assert report.profit_units == -0.2
    assert report.total_staked_units == 3.0
    assert report.roi == -0.2 / 3.0


def test_report_is_safe_for_empty_input():
    report = run_team_progression_backtest([], min_history=5, top_n=5)

    assert report.bets == 0
    assert report.series_started == 0
    assert report.series_completed == 0
    assert report.hit_rate == 0.0
    assert report.completion_rate == 0.0
    assert report.max_capital_units == 0
    assert report.busts == 0
    assert report.profit_units is None
    assert report.roi is None


def test_invalid_draw_odds_are_rejected():
    matches = [_match(1, "A", "B", "H")]

    try:
        run_team_progression_backtest(matches, draw_odds=1.0)
    except ValueError as exc:
        assert str(exc) == "draw_odds must be greater than 1.0"
    else:
        raise AssertionError("expected invalid draw odds to raise ValueError")
