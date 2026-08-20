from datetime import date

from spm.backtest.split import temporal_split
from spm.data.schema import HistoricalMatch


def test_temporal_split_is_strictly_chronological():
    rows = [
        HistoricalMatch(date(2020,1,1), "A", "2020", "X", "Y", 1, 0),
        HistoricalMatch(date(2021,1,1), "A", "2021", "X", "Y", 1, 1),
        HistoricalMatch(date(2022,1,1), "A", "2022", "X", "Y", 0, 1),
    ]
    split = temporal_split(rows, train_end=date(2020,12,31), validation_end=date(2021,12,31))
    assert len(split.train) == len(split.validation) == len(split.oos) == 1
