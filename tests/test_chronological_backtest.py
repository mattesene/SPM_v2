from datetime import date

from spm.backtest.engine import ChronologicalBacktester
from spm.data.models import Match


def test_backtester_requires_history_before_scoring():
    engine = ChronologicalBacktester(min_history=3)
    matches = [
        Match(date(2025, 1, 1), "A", "B", 1, 0),
        Match(date(2025, 1, 2), "B", "C", 1, 1),
        Match(date(2025, 1, 3), "A", "C", 0, 0),
    ]
    observations = engine.run(matches)
    assert len(observations) == 2
