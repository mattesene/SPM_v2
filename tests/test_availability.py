from urllib.error import HTTPError

from spm.data.availability import check_catalog_urls
from spm.data.historical_catalog import HistoricalCatalog, SeasonSource


def test_availability_handles_http_error(monkeypatch):
    def fake_urlopen(*args, **kwargs):
        raise HTTPError("https://example.test/x.csv", 404, "not found", {}, None)

    monkeypatch.setattr("spm.data.availability.urlopen", fake_urlopen)
    catalog = HistoricalCatalog((SeasonSource("E0", "2425", "https://example.test/x.csv", "x.csv"),))
    result = check_catalog_urls(catalog)
    assert result[0].available is False
    assert result[0].status == 404
