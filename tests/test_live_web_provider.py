import json
from datetime import date

from spm.live.web_provider import JSONFixtureProvider


def test_json_fixture_provider_parses_fixture_payload(monkeypatch):
    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return json.dumps({"fixtures": [{"home": "A", "away": "B", "kickoff": "2026-08-24"}]}).encode()

    monkeypatch.setattr("spm.live.web_provider.urlopen", lambda request, timeout: Response())
    result = JSONFixtureProvider("https://example.invalid/feed").fetch_fixtures(date(2026, 8, 23))
    assert result[0].home == "A"
    assert result[0].away == "B"
