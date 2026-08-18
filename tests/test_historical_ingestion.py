from datetime import date

from spm.ingestion.historical import fetch_seasons
from spm.ingestion.protocol import FetchBatch
from spm.data.normalized import MatchRecord


class FakeAdapter:
    def __init__(self):
        self.calls = []

    def fetch(self, season, competition):
        self.calls.append((season, competition))
        return FetchBatch("fake", None, (MatchRecord(date(2025, 8, 1), "A", "B", 1, 1, competition, season),))


def test_fetch_seasons_fetches_every_requested_slice():
    adapter = FakeAdapter()
    records = fetch_seasons(["2425", "2526"], ["I1", "E0"], adapter)
    assert len(records) == 4
    assert adapter.calls == [("2425", "I1"), ("2425", "E0"), ("2526", "I1"), ("2526", "E0")]
