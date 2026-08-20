from datetime import date

import pytest

from spm.data.match_odds import attach_draw_odds
from spm.data.models import Match
from spm.data.odds import DrawOdds


def test_attach_draw_odds_matches_exact_key():
    match = Match(date(2024, 1, 1), "A", "B", 1, 1)
    odds = DrawOdds(date(2024, 1, 1), "A", "B", 3.2)
    result = attach_draw_odds((match,), (odds,))
    assert result[0].draw_odds == 3.2


def test_attach_draw_odds_rejects_conflicting_duplicates():
    match = Match(date(2024, 1, 1), "A", "B", 1, 1)
    odds = (DrawOdds(date(2024, 1, 1), "A", "B", 3.2), DrawOdds(date(2024, 1, 1), "A", "B", 3.4))
    with pytest.raises(ValueError, match="ambiguous"):
        attach_draw_odds((match,), odds)
