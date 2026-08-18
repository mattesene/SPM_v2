import pytest

from spm.ingestion.seasons import season_codes


def test_default_historical_range_is_2019_20_through_2025_26():
    assert season_codes() == ("1920", "2021", "2122", "2223", "2324", "2425", "2526")


def test_season_range_rejects_inverted_bounds():
    with pytest.raises(ValueError):
        season_codes(2025, 2019)
