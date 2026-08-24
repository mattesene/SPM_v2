"""HTTP provider adapters for public fixture endpoints."""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
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
        request = Request(self.url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
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


class SofaScoreFixtureProvider:
    """Read upcoming fixtures from SofaScore's public scheduled-events API."""

    BASE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{day}"
    ALLOWED_TOURNAMENTS = {
        "Premier League",
        "Championship",
        "Bundesliga",
        "Serie A",
        "LaLiga",
    }

    def __init__(self, *, days: int = 7, timeout: int = 20) -> None:
        self.days = max(1, days)
        self.timeout = timeout

    def fetch_fixtures(self, from_date: date) -> list[RawFixture]:
        result: list[RawFixture] = []
        seen: set[tuple[date, str, str]] = set()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.sofascore.com/",
            "Origin": "https://www.sofascore.com",
        }
        for offset in range(self.days):
            day = from_date + timedelta(days=offset)
            request = Request(self.BASE_URL.format(day=day.isoformat()), headers=headers)
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    payload = json.load(response)
            except HTTPError as exc:
                raise FixtureProviderError(f"SofaScore HTTP {exc.code} for {day}") from exc
            except URLError as exc:
                raise FixtureProviderError(f"SofaScore unavailable for {day}: {exc.reason}") from exc
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise FixtureProviderError(f"SofaScore returned invalid JSON for {day}") from exc

            for event in payload.get("events", []):
                status = (event.get("status") or {}).get("type")
                if status not in {None, "notstarted"}:
                    continue
                tournament = ((event.get("tournament") or {}).get("name") or "").strip()
                unique = ((event.get("tournament") or {}).get("uniqueTournament") or {}).get("name", "")
                if tournament not in self.ALLOWED_TOURNAMENTS and unique not in self.ALLOWED_TOURNAMENTS:
                    continue
                home = ((event.get("homeTeam") or {}).get("name") or "").strip()
                away = ((event.get("awayTeam") or {}).get("name") or "").strip()
                if not home or not away:
                    continue
                timestamp = event.get("startTimestamp")
                kickoff = day
                if timestamp:
                    kickoff = datetime.fromtimestamp(int(timestamp), tz=timezone.utc).date()
                key = (kickoff, home, away)
                if kickoff >= from_date and key not in seen:
                    seen.add(key)
                    result.append(RawFixture(home, away, kickoff))
        return result
