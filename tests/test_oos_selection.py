import pytest

from spm.backtest.oos_selection import OOSCandidate, select_top_oos_candidates


def candidate(key: str, score: float, bets: int = 10) -> OOSCandidate:
    return OOSCandidate(key, bets, 5, 100.0, 0.10, 10.0, 20.0, score)


def test_selects_at_most_five_and_orders_by_score():
    result = select_top_oos_candidates([candidate(str(i), float(i)) for i in range(8)])
    assert [item.key for item in result] == ["7", "6", "5", "4", "3"]


def test_filters_candidates_below_minimum_sample():
    result = select_top_oos_candidates([candidate("weak", 100.0, 4), candidate("ok", 1.0, 5)])
    assert [item.key for item in result] == ["ok"]


def test_duplicate_keys_keep_best_score():
    result = select_top_oos_candidates([candidate("A", 1.0), candidate("A", 2.0), candidate("B", 1.5)])
    assert [item.key for item in result] == ["A", "B"]


def test_ties_are_deterministic_by_key():
    result = select_top_oos_candidates([candidate("B", 1.0), candidate("A", 1.0)])
    assert [item.key for item in result] == ["A", "B"]
