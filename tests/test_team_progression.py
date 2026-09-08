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
    # The series commits 1 unit on the first bet and 2 on the next one.
    assert report.max_capital_units == 3


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

    # Bet 1 loses (-1); bet 2 wins (+2 * (3 - 1)), for +3 units overall.
    assert report.profit_units == 3.0
    assert report.total_staked_units == 3.0
    assert report.roi == 1.0
    assert report.max_drawdown_units == 1.0
    assert report.draw_odds == 3.0


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
