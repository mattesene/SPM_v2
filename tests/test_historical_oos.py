from datetime import date

import pytest

from spm.backtest.historical_oos import evaluate_historical_oos
from spm.backtest.windows import OOSWindow
from spm.data.historical_catalog import HistoricalCatalog
from spm.data.season_urls import SeasonSource


def test_historical_oos_rejects_empty_catalog(tmp_path):
    source = SeasonSource("E0", "2021", "https://example.invalid/x.csv", "x.csv")
    catalog = HistoricalCatalog((source,))
    window = OOSWindow(date(2020,1,1), date(2020,2,1), date(2020,2,1), date(2020,3,1), date(2020,3,1))
    with pytest.raises(FileNotFoundError):
        evaluate_historical_oos(catalog, tmp_path, (window,))
