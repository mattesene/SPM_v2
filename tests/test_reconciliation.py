from datetime import date

import pytest

from spm.data.normalized import MatchRecord
from spm.data.provenance import Provenance
from spm.data.reconcile import reconcile


def test_reconcile_merges_aliases_and_provenance() -> None:
    records = [
        MatchRecord(date(2026, 8, 8), "Inter Milan", "AC Milan", 2, 1, "Serie A", "2026/27", (Provenance("sofascore", "1"),)),
        MatchRecord(date(2026, 8, 8), "Internazionale", "Milan", 2, 1, "Serie A", "2026/27", (Provenance("fbref", "2"),)),
    ]
    result = reconcile(records)
    assert len(result) == 1
    assert result[0].home_goals == 2
    assert result[0].source_count == 2


def test_reconcile_rejects_conflicting_scores() -> None:
    records = [
        MatchRecord(date(2026, 8, 8), "Inter", "Milan", 2, 1, "Serie A", "2026/27"),
        MatchRecord(date(2026, 8, 8), "Inter", "Milan", 1, 1, "Serie A", "2026/27"),
    ]
    with pytest.raises(ValueError, match="Conflicting scores"):
        reconcile(records)
