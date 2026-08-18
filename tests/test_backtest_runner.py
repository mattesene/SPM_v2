from datetime import date

import pytest

from spm.backtest.runner import run_slice
from spm.data.normalized import MatchRecord


def test_run_slice_keeps_competition_and_season():
    records = [MatchRecord(date(2025, 8, 1), "A", "B", 1, 1, "I1", "2526")]
    result = run_slice(records)
    assert result.competition == "I1"
    assert result.season == "2526"
    assert result.report.samples == 0


def test_run_slice_rejects_mixed_slices():
    records = [
        MatchRecord(date(2025, 8, 1), "A", "B", 1, 1, "I1", "2526"),
        MatchRecord(date(2025, 8, 2), "C", "D", 1, 0, "E0", "2526"),
    ]
    with pytest.raises(ValueError):
        run_slice(records)
