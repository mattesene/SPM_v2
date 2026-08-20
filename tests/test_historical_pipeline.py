from pathlib import Path

from spm.data.historical_pipeline import prepare_historical_scope
from spm.data.historical_scope import default_historical_scope


def test_prepare_historical_scope_reports_missing_files(tmp_path: Path, monkeypatch):
    scope = default_historical_scope(tmp_path)

    def fake_download_catalog(catalog, root):
        return ()

    monkeypatch.setattr(
        "spm.data.historical_pipeline.download_catalog",
        fake_download_catalog,
    )

    result = prepare_historical_scope(scope)
    assert not result.complete
    assert result.missing
    assert result.downloads == ()
