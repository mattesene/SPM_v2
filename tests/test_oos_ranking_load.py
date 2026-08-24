import csv

import pytest

from spm.backtest.oos_ranking import load_oos_ranking


def test_load_oos_ranking_missing_file_is_empty(tmp_path):
    assert load_oos_ranking(tmp_path / "missing.csv") == ()


def test_load_oos_ranking_reads_valid_csv(tmp_path):
    path = tmp_path / "oos.csv"
    fields = [
        "key", "windows", "bets", "profit", "roi",
        "max_drawdown", "profitable_window_rate", "score",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "key": "Team A", "windows": 4, "bets": 20, "profit": 120,
            "roi": 0.12, "max_drawdown": 30,
            "profitable_window_rate": 0.75, "score": 0.205,
        })

    result = load_oos_ranking(path)
    assert len(result) == 1
    assert result[0].key == "Team A"
    assert result[0].bets == 20
    assert result[0].profit == pytest.approx(120.0)


def test_load_oos_ranking_rejects_malformed_csv(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("key,windows\nTeam A,not-a-number\n", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid OOS ranking row"):
        load_oos_ranking(path)
