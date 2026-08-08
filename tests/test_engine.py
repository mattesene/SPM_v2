from datetime import date

from spm.data.models import Match
from spm.statistics.engine import SPMEngine


def history() -> list[Match]:
    return [
        Match(date(2026, 7, 1), "A", "B", 1, 1),
        Match(date(2026, 7, 2), "C", "A", 0, 1),
        Match(date(2026, 7, 3), "B", "C", 0, 0),
        Match(date(2026, 7, 4), "A", "C", 1, 0),
        Match(date(2026, 7, 5), "B", "A", 1, 1),
        Match(date(2026, 7, 6), "C", "B", 1, 1),
    ]


def test_recent_form_is_used_by_engine() -> None:
    result = SPMEngine().score(history(), "A", "B", date(2026, 7, 10))
    assert 0 <= result.draw_probability <= 1
    assert 0 <= result.spm_score <= 100
    assert 0 <= result.form_balance <= 1
    assert 0 <= result.draw_signal <= 1
    assert 0 <= result.goal_balance_signal <= 1


def test_rank_is_descending() -> None:
    engine = SPMEngine()
    results = engine.rank(history(), [("A", "B"), ("B", "C")], date(2026, 7, 10))
    assert len(results) == 2
    assert results[0].spm_score >= results[1].spm_score
