from datetime import date

from spm.data.dedup import deduplicate_matches, group_duplicates
from spm.data.models import Match


def test_dedup_uses_normalized_team_names() -> None:
    first = Match(date(2026, 8, 1), "Bayern München", "FC Köln", 1, 1)
    second = Match(date(2026, 8, 1), "bayern munchen", "FC Koln", 1, 1)
    assert len(group_duplicates([first, second])) == 1
    assert deduplicate_matches([first, second]) == [first]


def test_dedup_preserves_different_scores_for_conflict_detection() -> None:
    first = Match(date(2026, 8, 1), "A", "B", 1, 1)
    second = Match(date(2026, 8, 1), "A", "B", 2, 1)
    groups = group_duplicates([first, second])
    assert len(groups) == 1
    assert len(groups[0].matches) == 2
