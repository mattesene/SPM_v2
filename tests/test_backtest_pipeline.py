from datetime import date

import pytest

from spm.backtest.pipeline import run_historical_pipeline
from spm.data.normalized import MatchRecord


class DummyEngine:
    def predict(self, home_team, away_team):
        return None

    def update(self, home_team, away_team, home_goals, away_goals):
        pass


def test_pipeline_runs_from_normalized_records():
    records = [MatchRecord(date(2025, 8, 1), "A", "B", 1, 1, "I1", "2526")]
    result = run_historical_pipeline(records, DummyEngine)
    assert len(result.slices) == 1
    assert result.slices[0].competition == "I1"


def test_pipeline_rejects_empty_data():
    with pytest.raises(ValueError):
        run_historical_pipeline([], DummyEngine)
