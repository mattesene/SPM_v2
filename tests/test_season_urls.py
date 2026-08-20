import pytest

from spm.data.season_urls import football_data_season


def test_builds_football_data_source():
    source = football_data_season("E0", "2425")
    assert source.filename == "E02425.csv"
    assert source.url.endswith("/2425/E02425.csv")


def test_normalizes_competition_code_case():
    source = football_data_season(" e0 ", "2425")
    assert source.competition == "E0"
    assert source.filename == "E02425.csv"


def test_rejects_invalid_season_code():
    with pytest.raises(ValueError):
        football_data_season("E0", "20245")
