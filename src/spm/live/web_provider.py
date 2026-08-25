"""HTTP provider adapters for public fixture endpoints."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
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


class _DirettaHTMLParser(HTMLParser):
    """Extract the stable participant/time classes used by Diretta.it."""

    def __init__(self, from_date: date) -> None:
        super().__init__(convert_charrefs=True)
        self.from_date = from_date
        self.current_class = ""
        self.buffer = ""
        self.home = ""
        self.away = ""
        self.time_text = ""
        self.fixtures: list[RawFixture] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class") or ""
        if "event__participant--home" in classes:
            self.current_class = "home"
            self.buffer = ""
        elif "event__participant--away" in classes:
            self.current_class = "away"
            self.buffer = ""
        elif "event__time" in classes:
            self.current_class = "time"
            self.buffer = ""

    def handle_data(self, data: str) -> None:
        if self.current_class:
            self.buffer += data

    def handle_endtag(self, tag: str) -> None:
        if not self.current_class:
            return
        value = " ".join(self.buffer.split())
        if self.current_class == "home":
            self.home = value
        elif self.current_class == "away":
            self.away = value
        elif self.current_class == "time":
            self.time_text = value
        self.current_class = ""
        self.buffer = ""
        if self.home and self.away and self.time_text:
            match = re.search(r"(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.?", self.time_text)
            if match:
                kickoff = date(self.from_date.year, int(match.group("month")), int(match.group("day")))
            else:
                kickoff = self.from_date
            if kickoff >= self.from_date:
                self.fixtures.append(RawFixture(self.home, self.away, kickoff))
            self.home = self.away = self.time_text = ""


class DirettaFixtureProvider:
    """Read upcoming fixtures from Diretta.it calendar pages as a fallback."""

    CALENDAR_URLS = (
        "https://www.diretta.it/serie-a/La/news/calendario/",
        "https://www.diretta.it/calcio/inghilterra/premier-league/calendario/",
        "https://www.diretta.it/calcio/inghilterra/championship/calendario/",
        "https://www.diretta.it/calcio/germania/bundesliga/calendario/",
        "https://www.diretta.it/calcio/spagna/laliga/calendario/",
    )

    def __init__(self, *, days: int = 7, timeout: int = 20) -> None:
        self.days = max(1, days)
        self.timeout = timeout

    def fetch_fixtures(self, from_date: date) -> list[RawFixture]:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
        }
        result: list[RawFixture] = []
        seen: set[tuple[date, str, str]] = set()
        latest = from_date + timedelta(days=self.days - 1)
        for url in self.CALENDAR_URLS:
            request = Request(url, headers=headers)
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    html = response.read().decode("utf-8", errors="replace")
            except HTTPError as exc:
                raise FixtureProviderError(f"Diretta.it HTTP {exc.code}") from exc
            except URLError as exc:
                raise FixtureProviderError(f"Diretta.it unavailable: {exc.reason}") from exc
            except TimeoutError as exc:
                raise FixtureProviderError("Diretta.it timeout") from exc

            parser = _DirettaHTMLParser(from_date)
            parser.feed(html)
            for fixture in parser.fixtures:
                if from_date <= fixture.kickoff <= latest:
                    key = (fixture.kickoff, fixture.home, fixture.away)
                    if key not in seen:
                        seen.add(key)
                        result.append(fixture)
        if not result:
            raise FixtureProviderError("Diretta.it returned no usable upcoming fixtures")
        return result


class FallbackFixtureProvider:
    """Try the primary provider and fall back to a secondary source."""

    def __init__(self, primary, fallback) -> None:
        self.primary = primary
        self.fallback = fallback

    def fetch_fixtures(self, from_date: date) -> list[RawFixture]:
        try:
            result = self.primary.fetch_fixtures(from_date)
            if result:
                return result
        except FixtureProviderError as exc:
            print(f"WARNING: primary Live provider failed: {exc}")
        try:
            result = self.fallback.fetch_fixtures(from_date)
            if result:
                print(f"Live fixture fallback: {len(result)} fixtures from Diretta.it")
                return result
        except FixtureProviderError as exc:
            raise FixtureProviderError(f"primary and fallback providers failed: {exc}") from exc
        raise FixtureProviderError("primary and fallback providers returned no fixtures")
