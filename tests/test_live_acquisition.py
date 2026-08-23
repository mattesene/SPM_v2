from datetime import date

from spm.data.fixtures import Fixture
from spm.data.repository import MatchRepository
from spm.live.acquisition import acquire_fixtures


class FakeProvider:
    def __init__(self, fixtures):
        self.fixtures = fixtures
        self.requested_from = None

    def fetch_fixtures(self, from_date):
        self.requested_from = from_date
        return self.fixtures


def test_acquire_fixtures_persists_provider_results(tmp_path):
    db = tmp_path / "spm.db"
    repo = MatchRepository(db)
    fixtures = [
        Fixture("H0", "A0", date(2026, 8, 24)),
        Fixture("H1", "A1", date(2026, 8, 25)),
    ]
    provider = FakeProvider(fixtures)

    result = acquire_fixtures(provider, repo, from_date=date(2026, 8, 23))

    assert provider.requested_from == date(2026, 8, 23)
    assert result.fixtures_seen == 2
    assert result.fixtures_written == 2
    assert repo.load_fixtures(from_date=date(2026, 8, 23)) == fixtures
