from pathlib import Path

import pytest

from spm.live.data_manifest import validate_live_inputs


def test_validate_live_inputs_accepts_non_empty_files(tmp_path: Path) -> None:
    db = tmp_path / "spm.db"
    oos = tmp_path / "oos.csv"
    db.write_bytes(b"sqlite")
    oos.write_text("fixture,bets\n", encoding="utf-8")
    manifest = validate_live_inputs(db, oos)
    assert manifest.database == db
    assert manifest.oos == oos


def test_validate_live_inputs_rejects_missing_file(tmp_path: Path) -> None:
    db = tmp_path / "missing.db"
    oos = tmp_path / "oos.csv"
    oos.write_text("fixture,bets\n", encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        validate_live_inputs(db, oos)


def test_validate_live_inputs_rejects_empty_file(tmp_path: Path) -> None:
    db = tmp_path / "spm.db"
    oos = tmp_path / "oos.csv"
    db.write_bytes(b"")
    oos.write_text("fixture,bets\n", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_live_inputs(db, oos)
