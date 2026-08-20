from datetime import date

from spm.data.normalization_adapter import canonicalize_matches
from spm.data.schema import HistoricalMatch


def test_canonicalize_matches_maps_provider_aliases():
    match = HistoricalMatch(date(2025, 1, 1), "Serie A", "2025", "Internazionale Milano", "AS Roma", 1, 1, 3.2)
    result = canonicalize_matches([match])
    assert result[0].home_team == "inter"
    assert result[0].away_team == "roma"
