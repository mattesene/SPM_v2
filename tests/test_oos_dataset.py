from datetime import date

from spm.backtest.oos_dataset import build_team_staking_dataset
from spm.data.models import Match
from spm.data.odds import DrawOdds


def test_builds_team_datasets_from_matches_and_odds():
    matches = [Match(date(2026, 8, 1), "A", "B", 1, 1)]
    odds = [DrawOdds(date(2026, 8, 1), "A", "B", 3.2)]
    result = build_team_staking_dataset(matches, odds)
    assert result["A"] == [("A", True, 3.2)]
    assert result["B"] == [("B", True, 3.2)]


def test_missing_odds_are_preserved_as_none():
    matches = [Match(date(2026, 8, 1), "A", "B", 2, 1)]
    result = build_team_staking_dataset(matches, [])
    assert result["A"] == [("A", False, None)]
    assert result["B"] == [("B", False, None)]
