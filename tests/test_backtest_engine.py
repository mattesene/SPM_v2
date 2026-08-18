from datetime import date

import pytest

from spm.backtest import ChronologicalBacktester
from spm.data.models import Match


def test_backtest_never_uses_current_match_for_prediction():
    matches = [
        Match(date(2024, 1, 1), "A", "B", 0, 0),
        Match(date(2024, 1, 8), "A", "C", 2, 0),
        Match(date(2024, 1, 15), "B", "C", 1, 1),
        Match(date(2024, 1, 22), "A", "B", 0, 1),
    ]
    observations = ChronologicalBacktester(min_history=1).run(matches)
    assert len(observations) == 3
    assert observations[-1].home_team == "A"
    assert observations[-1].away_team == "B"


def test_backtest_respects_minimum_history():
    matches = [
        Match(date(2024, 1, 1), "A", "B", 0, 0),
        Match(date(2024, 1, 8), "A", "C", 1, 0),
        Match(date(2024, 1, 15), "B", "C", 1, 1),
    ]
    assert ChronologicalBacktester(min_history=2).run(matches) == ()


def test_invalid_threshold():
    with pytest.raises(ValueError):
        ChronologicalBacktester(threshold=1.1)
