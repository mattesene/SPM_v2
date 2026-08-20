from datetime import date, timedelta

from spm.data.schema import HistoricalMatch
from spm.data.sequence_builder import build_team_features


def test_features_use_only_previous_matches():
    rows = (
        HistoricalMatch(date(2025,1,1), "A", "2025", "X", "Y", 1, 0),
        HistoricalMatch(date(2025,1,2), "A", "2025", "X", "Z", 2, 0),
        HistoricalMatch(date(2025,1,3), "A", "2025", "X", "Y", 1, 1),
    )
    features = build_team_features(rows)
    x = [r for r in features if r.team == "X"]
    assert [r.draw_streak_before for r in x] == [0, 1, 2]


def test_draw_resets_streak():
    rows = (
        HistoricalMatch(date(2025,1,1), "A", "2025", "X", "Y", 1, 0),
        HistoricalMatch(date(2025,1,2), "A", "2025", "X", "Z", 1, 1),
        HistoricalMatch(date(2025,1,3), "A", "2025", "X", "Y", 1, 0),
    )
    x = [r for r in build_team_features(rows) if r.team == "X"]
    assert [r.draw_streak_before for r in x] == [0, 1, 0]
