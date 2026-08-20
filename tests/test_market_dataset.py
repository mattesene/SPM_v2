from datetime import date

import pytest

from spm.data.market_dataset import attach_draw_odds
from spm.data.normalized import MatchRecord
from spm.data.odds import DrawOdds


def _match() -> MatchRecord:
    return MatchRecord(
        date=date(2025, 1, 1),
        home_team="Milan",
        away_team="Roma",
        home_goals=1,
        away_goals=1,
    )


def test_attach_draw_odds_to_normalized_match():
    result = attach_draw_odds([_match()], [DrawOdds(date(2025, 1, 1), "Milan", "Roma", 3.2, "test")])
    assert result[0].draw_odds == 3.2


def test_attach_rejects_missing_odds():
    with pytest.raises(ValueError, match="missing draw odds"):
        attach_draw_odds([_match()], [])
