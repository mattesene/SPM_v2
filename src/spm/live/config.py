"""Configuration for selecting a Live fixture provider."""
from __future__ import annotations

import os

from spm.live.providers import CSVFixtureProvider
from spm.live.web_provider import JSONFixtureProvider, SofaScoreFixtureProvider


def build_fixture_provider():
    provider = os.getenv("SPM_LIVE_PROVIDER", "sofascore").strip().lower()
    if provider == "csv":
        path = os.getenv("SPM_LIVE_FIXTURES", "data/live/fixtures.csv")
        return CSVFixtureProvider(path)
    if provider == "json":
        url = os.getenv("SPM_LIVE_FIXTURES_URL", "").strip()
        if not url:
            raise ValueError("SPM_LIVE_FIXTURES_URL is required for json provider")
        return JSONFixtureProvider(url)
    if provider == "sofascore":
        days = int(os.getenv("SPM_LIVE_DAYS", "7"))
        timeout = int(os.getenv("SPM_LIVE_TIMEOUT", "20"))
        return SofaScoreFixtureProvider(days=days, timeout=timeout)
    raise ValueError(f"unsupported Live provider: {provider}")
