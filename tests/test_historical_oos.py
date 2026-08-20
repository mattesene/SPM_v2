from datetime import date

import pytest

from spm.backtest.historical_oos import evaluate_historical_oos
from spm.backtest.windows import OOSWindow
from spm.data.historical_catalog import HistoricalCatalog, HistoricalSource


def test_historical_oos_rejects_empty_catalog(tmp_path):
    catalog = HistoricalCatalog((HistoricalSource("E0", "2020-21", "x.csv", "https://example.invalid/x.csv"),))
    window = OOSWindow(date(2020,1,1), date(2020,2,1), date(2020,2,1), date(2020,3,1), date(2020,3,1))
    with pytest.raises(FileNotFoundError):
        evaluate_historical_oos(catalog, tmp_path, (window,))
