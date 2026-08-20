"""Public-source availability helpers for historical datasets."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .historical_catalog import HistoricalCatalog


@dataclass(frozen=True, slots=True)
class Availability:
    competition: str
    season: str
    url: str
    available: bool
    status: int | None


def check_catalog_urls(catalog: HistoricalCatalog, *, timeout: float = 10.0) -> tuple[Availability, ...]:
    results: list[Availability] = []
    for source in catalog.sources:
        request = Request(source.url, method="HEAD", headers={"User-Agent": "SPM_v2/1.0"})
        try:
            with urlopen(request, timeout=timeout) as response:
                results.append(Availability(source.competition, source.season, source.url, 200 <= response.status < 400, response.status))
        except HTTPError as exc:
            results.append(Availability(source.competition, source.season, source.url, False, exc.code))
        except (URLError, TimeoutError):
            results.append(Availability(source.competition, source.season, source.url, False, None))
    return tuple(results)
