from datetime import date

from spm.data.normalization import canonical_team_name, normalize_team_name
from spm.data.normalized import MatchRecord


def test_team_names_are_normalized_deterministically() -> None:
    assert normalize_team_name("  A.C. Milan  ") == "a c milan"
    assert canonical_team_name("AC Milan") == "milan"
    assert canonical_team_name("Internazionale Milano") == "inter"


def test_identity_uses_canonical_team_names() -> None:
    a = MatchRecord(date(2026, 8, 8), "Inter Milan", "AC Milan", competition="Serie A")
    b = MatchRecord(date(2026, 8, 8), "Internazionale", "Milan", competition="Serie A")
    assert a.identity_key == b.identity_key
