from datetime import date
from types import SimpleNamespace

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


def test_active_progression_continues_after_team_falls_out_of_top_n():
    class ScheduledEngine:
        def rank(self, history, fixtures, as_of, *, eligible_teams):
            selected_team = "A" if as_of.day == 6 else "B"
            return [SimpleNamespace(selected_team=selected_team, team_probability=0.90)]

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
        _match(7, "A", "B", "D"),
    ]

    report = run_team_progression_backtest(
        matches, min_history=5, top_n=1, engine=ScheduledEngine()
    )

    # Day 6 starts A's progression. On day 7 the daily top-1 selection is B,
    # but A is still active and must be followed at stake 2.
    a_observations = [observation for observation in report.observations if observation.team == "A"]
    assert len(a_observations) == 2
    assert a_observations[0].date == date(2025, 1, 6)
    assert a_observations[0].stake_units == 1
    assert a_observations[1].date == date(2025, 1, 7)
    assert a_observations[1].stake_units == 2
    assert a_observations[1].streak_before == 1
    assert report.series_started == 1
    assert report.series_completed == 1


def test_max_capital_tracks_multiple_open_progressions():
    class FixedEngine:
        def rank(self, history, fixtures, as_of, *, eligible_teams):
            return [
                SimpleNamespace(selected_team="A", team_probability=0.90),
                SimpleNamespace(selected_team="B", team_probability=0.80),
                SimpleNamespace(selected_team="C", team_probability=0.70),
            ]

    matches = [
        *[_match(day, "A", f"A{day}", "H") for day in range(1, 6)],
        *[_match(day, "B", f"B{day}", "H") for day in range(1, 6)],
        *[_match(day, "C", f"C{day}", "H") for day in range(1, 6)],
        _match(6, "A", "B", "H"),
        _match(6, "C", "D", "H"),
        _match(7, "A", "B", "D"),
        _match(7, "C", "E", "H"),
    ]

    report = run_team_progression_backtest(
        matches, min_history=5, top_n=3, engine=FixedEngine()
    )

    # Three series open on day 6. After the losses, each requires a 2-unit
    # next stake, so committed capital reaches 9. On day 7 A and B close,
    # while C remains open.
    assert report.series_started == 3
    assert report.series_completed == 2
    assert report.max_stake_units == 2
    assert report.max_capital_units == 9
    assert report.bets == 5


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



def test_odds_sensitivity_reuses_same_observations():
    from spm.backtest.team_progression import evaluate_odds_sensitivity

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
    report = run_team_progression_backtest(matches, min_history=5, top_n=1)

    sensitivity = evaluate_odds_sensitivity(report.observations, (1.4, 2.0, 3.0))

    assert sensitivity[1.4]["profit_units"] == -0.2
    assert sensitivity[2.0]["profit_units"] == 0.0
    assert sensitivity[3.0]["profit_units"] == 3.0
    assert sensitivity[3.0]["total_staked_units"] == 3.0
    assert sensitivity[3.0]["roi"] == 1.0
    assert sensitivity[3.0]["max_drawdown_units"] == 1.0


def test_odds_sensitivity_rejects_invalid_values():
    from spm.backtest.team_progression import evaluate_odds_sensitivity

    try:
        evaluate_odds_sensitivity((), (1.0,))
    except ValueError as exc:
        assert str(exc) == "all odds values must be greater than 1.0"
    else:
        raise AssertionError("expected invalid sensitivity odds to raise ValueError")


def test_aggregate_economic_reports_keeps_drawdown_dataset_scoped():
    from spm.backtest.team_progression import TeamProgressionReport, aggregate_economic_reports

    reports = (
        TeamProgressionReport((), 1, 1, 1, 1, 0, 0, 1, 1, 0, 2.0, 1.0, 2.0, 2.0),
        TeamProgressionReport((), 1, 1, 1, 1, 0, 0, 4, 7, 0, 3.0, 2.0, 5.0, 3.0),
    )
    result = aggregate_economic_reports(reports)

    assert result["profit_units"] == 5.0
    assert result["total_staked_units"] == 3.0
    assert result["roi"] == 5.0 / 3.0
    assert result["max_dataset_drawdown_units"] == 5.0
    assert result["max_dataset_capital_units"] == 7
