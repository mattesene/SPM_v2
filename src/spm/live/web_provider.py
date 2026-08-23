"""HTTP provider adapter for public fixture endpoints returning JSON."""
from __future__ import annotations

import json
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from spm.live.normalization import RawFixture


class FixtureProviderError(RuntimeError):
    """A recoverable upstream fixture-source error."""


class JSONFixtureProvider:
    def __init__(self, url: str, *, timeout: int = 20) -> None:
        self.url = url
        self.timeout = timeout

    def fetch_fixtures(self, from_date: date) -> list[RawFixture]:
        request = Request(self.url, headers={"User-Agent": "SPM_v2/1.0"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.load(response)
        except HTTPError as exc:
            raise FixtureProviderError(f"HTTP {exc.code} from fixture source") from exc
        except URLError as exc:
            raise FixtureProviderError(f"fixture source unavailable: {exc.reason}") from exc
        except TimeoutError as exc:
            raise FixtureProviderError("fixture source timeout") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise FixtureProviderError("fixture source returned invalid JSON") from exc

        rows = payload.get("fixtures", payload) if isinstance(payload, dict) else payload
        if not isinstance(rows, list):
            raise FixtureProviderError("fixture source returned an invalid payload")

        result: list[RawFixture] = []
        try:
            for row in rows:
                kickoff = date.fromisoformat(row["kickoff"])
                if kickoff >= from_date:
                    result.append(RawFixture(row["home"], row["away"], kickoff))
        except (KeyError, TypeError, ValueError) as exc:
            raise FixtureProviderError("fixture source contains an invalid row") from exc
        return result
