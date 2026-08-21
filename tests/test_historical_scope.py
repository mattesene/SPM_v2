from pathlib import Path

from spm.data.historical_scope import default_historical_scope


def test_default_scope_contains_expected_35_sources(tmp_path: Path):
    scope = default_historical_scope(tmp_path)
    assert len(scope.catalog.sources) == 35
    assert len(scope.expected_files) == 35
    assert not scope.complete


def test_scope_detects_complete_cache(tmp_path: Path):
    scope = default_historical_scope(tmp_path)
    for path in scope.expected_files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder", encoding="utf-8")
    assert scope.complete
    assert scope.missing_files == ()
