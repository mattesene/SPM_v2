"""HTTP provider adapter for public fixture endpoints returning JSON."""
from __future__ import annotations

import json
from datetime import date
from urllib.request import Request, urlopen

from spm.live.normalization import RawFixture


class JSONFixtureProvider:
    def __init__(self, url: str, *, timeout: int = 20) -> None:
        self.url = url
        self.timeout = timeout

    def fetch_fixtures(self, from_date: date) -> list[RawFixture]:
        request = Request(self.url, headers={"User-Agent": "SPM_v2/1.0"})
        with urlopen(request, timeout=self.timeout) as response:
            payload = json.load(response)
        rows = payload.get("fixtures", payload) if isinstance(payload, dict) else payload
        result = []
        for row in rows:
            kickoff = date.fromisoformat(row["kickoff"])
            if kickoff >= from_date:
                result.append(RawFixture(row["home"], row["away"], kickoff))
        return result
