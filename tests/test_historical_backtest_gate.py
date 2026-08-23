from pathlib import Path

import pytest

from scripts.run_historical_backtest import main


def test_default_historical_backtest_requires_complete_scope(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "scripts.run_historical_backtest.prepare_historical_scope",
        lambda scope: type("Result", (), {"complete": False, "missing": [Path("missing.csv")]})(),
    )

    with pytest.raises(RuntimeError, match="Historical dataset scope incomplete"):
        main()
