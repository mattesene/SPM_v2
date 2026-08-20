from datetime import date
import pytest

from spm.data.schema import HistoricalMatch
from spm.data.validation import validate_matches


def match(day, home="A", away="B"):
    return HistoricalMatch(day, "Serie A", "2025", home, away, 1, 1, 3.2)


def test_validation_sorts_matches_chronologically():
    result = validate_matches([match(date(2025, 2, 2)), match(date(2025, 1, 1))])
    assert result[0].match_date == date(2025, 1, 1)


def test_validation_rejects_duplicate_matches():
    with pytest.raises(ValueError, match="duplicate"):
        validate_matches([match(date(2025, 1, 1)), match(date(2025, 1, 1))])


def test_draw_property():
    assert match(date(2025, 1, 1)).is_draw
