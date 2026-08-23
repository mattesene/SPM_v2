import json
from datetime import date
from urllib.error import HTTPError

import pytest

from spm.live.web_provider import FixtureProviderError, JSONFixtureProvider


def test_http_error_is_wrapped(monkeypatch):
    def fail(request, timeout):
        raise HTTPError(request.full_url, 404, "missing", {}, None)
    monkeypatch.setattr("spm.live.web_provider.urlopen", fail)
    with pytest.raises(FixtureProviderError, match="HTTP 404"):
        JSONFixtureProvider("https://example.invalid/feed").fetch_fixtures(date(2026, 8, 23))


def test_invalid_json_is_wrapped(monkeypatch):
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return b"not-json"
    monkeypatch.setattr("spm.live.web_provider.urlopen", lambda request, timeout: Response())
    monkeypatch.setattr("json.load", lambda response: (_ for _ in ()).throw(json.JSONDecodeError("bad", "", 0)))
    with pytest.raises(FixtureProviderError, match="invalid JSON"):
        JSONFixtureProvider("https://example.invalid/feed").fetch_fixtures(date(2026, 8, 23))
