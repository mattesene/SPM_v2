from pathlib import Path

from spm.data.historical_catalog import HistoricalCatalog
from spm.data.season_urls import SeasonSource
from spm.data.historical_download import download_catalog


def test_download_catalog_uses_competition_season_cache(tmp_path: Path, monkeypatch):
    calls = []

    def fake_download(url, destination, *, force=False):
        calls.append((url, Path(destination)))
        return type("Result", (), {"path": Path(destination), "downloaded": True, "url": url})()

    monkeypatch.setattr("spm.data.historical_download.download_cached", fake_download)
    catalog = HistoricalCatalog((SeasonSource("e0", "2425", "https://example/e0.csv", "e02425.csv"),))
    download_catalog(catalog, tmp_path)
    assert calls[0][1] == tmp_path / "e0" / "2425" / "e02425.csv"
