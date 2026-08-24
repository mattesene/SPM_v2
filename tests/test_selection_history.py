from datetime import date

from spm.live.selection_history import LiveSelection, append_selections, load_selections


def test_selection_history_round_trip(tmp_path):
    path = tmp_path / "history.csv"
    item = LiveSelection(date(2026, 8, 24), 1, "A", "B", date(2026, 8, 25), 0.42, 3.1, 0.8, 0.6, 0.72)
    append_selections(path, [item])
    assert load_selections(path) == (item,)


def test_selection_history_missing_file_is_empty(tmp_path):
    assert load_selections(tmp_path / "missing.csv") == ()
