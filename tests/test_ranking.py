from datetime import date

from spm.data.models import Match
from spm.data.season import Season
from spm.statistics.ranking import Fixture, rank_draws


def test_rank_draws_descending() -> None:
    season = Season([
        Match(date(2026, 8, 1), "A", "B", 1, 1),
        Match(date(2026, 8, 2), "A", "C", 0, 0),
        Match(date(2026, 8, 3), "B", "C", 3, 0),
    ])
    result = rank_draws(season, [Fixture("A", "B"), Fixture("A", "C")])
    assert result[0].probability >= result[1].probability
