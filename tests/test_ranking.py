from datetime import date

from spm.data.models import Match
from spm.data.season import Season
from spm.statistics.ranking import Fixture, rank_draws
from spm.backtest.aggregation import TeamOOSStats
from spm.backtest.ranking import rank_teams, wilson_lower_bound
import pytest


def test_rank_draws_descending() -> None:
    season = Season([
        Match(date(2026, 8, 1), "A", "B", 1, 1),
        Match(date(2026, 8, 2), "A", "C", 0, 0),
        Match(date(2026, 8, 3), "B", "C", 3, 0),
    ])
    result = rank_draws(season, [Fixture("A", "B"), Fixture("A", "C")])
    assert result[0].probability >= result[1].probability


def test_wilson_lower_bound_is_below_observed_rate():
    assert wilson_lower_bound(18, 20) < .9
    assert wilson_lower_bound(18, 20) > 0


def test_top_five_excludes_small_samples():
    stats = [TeamOOSStats("A", 30, 30, 27, .9), TeamOOSStats("B", 10, 10, 10, 1.0)]
    result = rank_teams(stats, min_selections=20, top_n=5)
    assert [x.team for x in result] == ["A"]


def test_invalid_wilson_counts():
    with pytest.raises(ValueError):
        wilson_lower_bound(3, 2)
