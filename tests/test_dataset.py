from datetime import date
import pytest

from spm.data.dataset import join_results_and_odds
from spm.data.odds import DrawOdds
from spm.data.results import MatchResult


def _result():
    return MatchResult(date(2025, 1, 1), " Milan ", "Roma", 1, 1)


def _odds(value=3.2):
    return DrawOdds(date(2025, 1, 1), "Milan", "Roma", value)


def test_join_is_case_and_whitespace_insensitive():
    joined = join_results_and_odds((_result(),), (_odds(),))
    assert joined[0].odds.draw_odds == 3.2


def test_missing_odds_is_rejected():
    with pytest.raises(ValueError, match="missing odds"):
        join_results_and_odds((_result(),), ())


def test_conflicting_duplicate_odds_are_rejected():
    with pytest.raises(ValueError, match="conflicting odds"):
        join_results_and_odds((_result(),), (_odds(3.2), _odds(3.4)))
