from datetime import date

from spm.live.selection_history import LiveSelection, append_selections, load_selections


def test_append_selections_does_not_duplicate_same_snapshot(tmp_path):
    path = tmp_path / "history.csv"
    row = LiveSelection(date(2026, 8, 24), 1, "A", "B", date(2026, 8, 25), .4, None, .8, None, .8)
    append_selections(path, [row])
    append_selections(path, [row])
    assert load_selections(path) == (row,)
