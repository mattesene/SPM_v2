from datetime import date

from spm.data.models import Match
from spm.data.season import Season
from spm.statistics.model import PareggioModel


def test_team_stats_and_draw_prediction() -> None:
    season = Season(
        [
            Match(date(2026, 8, 1), "A", "B", 1, 1),
            Match(date(2026, 8, 2), "A", "C", 2, 0),
            Match(date(2026, 8, 3), "B", "C", 0, 0),
        ]
    )

    stats = season.team_stats("A")
    assert stats.matches == 2
    assert stats.goals_for == 3
    assert stats.goals_against == 1
    assert stats.draw_rate == 0.5

    prediction = PareggioModel().predict(season, "A", "B")
    assert prediction.home_team == "A"
    assert prediction.away_team == "B"
    assert 0.0 <= prediction.probability <= 1.0
    assert prediction.expected_home_goals > 0
    assert prediction.expected_away_goals >= 0
