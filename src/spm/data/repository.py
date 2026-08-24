"""SQLite persistence for normalized SPM records, fixtures and statistics."""
import sqlite3
from datetime import date
from pathlib import Path

from .fixtures import Fixture
from .models import Match
from .normalized import MatchRecord
from .stats import MatchStats


class MatchRepository:
    def __init__(self, path: str | Path = "spm.db") -> None:
        self.path = str(path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.execute("PRAGMA foreign_keys = ON")
        return db

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY, date TEXT NOT NULL, home_team TEXT NOT NULL,
                away_team TEXT NOT NULL, home_goals INTEGER, away_goals INTEGER,
                competition TEXT, season TEXT,
                UNIQUE(date, home_team, away_team, competition)
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS provenance (
                id INTEGER PRIMARY KEY, match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
                source TEXT NOT NULL, source_id TEXT, source_url TEXT, retrieved_at TEXT,
                UNIQUE(match_id, source, source_id)
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS match_stats (
                id INTEGER PRIMARY KEY, match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
                source TEXT NOT NULL, xg_home REAL, xg_away REAL,
                shots_home INTEGER, shots_away INTEGER, shots_on_target_home INTEGER, shots_on_target_away INTEGER,
                possession_home REAL, possession_away REAL, corners_home INTEGER, corners_away INTEGER,
                UNIQUE(match_id, source)
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS fixtures (
                id INTEGER PRIMARY KEY, date TEXT NOT NULL, home_team TEXT NOT NULL,
                away_team TEXT NOT NULL, refreshed_at TEXT NOT NULL,
                UNIQUE(date, home_team, away_team)
            )""")
            db.execute("CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(date)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_provenance_match ON provenance(match_id)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_stats_match ON match_stats(match_id)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_fixtures_date ON fixtures(date)")

    def _match_id(self, db: sqlite3.Connection, record: MatchRecord) -> int:
        row = db.execute(
            "SELECT id FROM matches WHERE date=? AND home_team=? AND away_team=? AND competition IS ?",
            (record.date.isoformat(), record.canonical_home_team, record.canonical_away_team, record.competition),
        ).fetchone()
        if row is None:
            raise RuntimeError("failed to locate match")
        return int(row[0])

    def upsert(self, record: MatchRecord) -> None:
        with self._connect() as db:
            db.execute(
                """INSERT INTO matches(date,home_team,away_team,home_goals,away_goals,competition,season)
                VALUES(?,?,?,?,?,?,?) ON CONFLICT(date,home_team,away_team,competition) DO UPDATE SET
                home_goals=COALESCE(excluded.home_goals,matches.home_goals),
                away_goals=COALESCE(excluded.away_goals,matches.away_goals),
                season=COALESCE(excluded.season,matches.season)""",
                (record.date.isoformat(), record.canonical_home_team, record.canonical_away_team,
                 record.home_goals, record.away_goals, record.competition, record.season),
            )
            match_id = self._match_id(db, record)
            for provenance in record.provenance:
                db.execute(
                    """INSERT OR IGNORE INTO provenance(match_id,source,source_id,source_url,retrieved_at)
                    VALUES(?,?,?,?,?)""",
                    (match_id, provenance.source, provenance.source_id, provenance.source_url,
                     provenance.retrieved_at.isoformat() if provenance.retrieved_at else None),
                )

    def upsert_stats(self, stats: MatchStats) -> None:
        with self._connect() as db:
            row = db.execute(
                "SELECT id FROM matches WHERE date=? AND home_team=? AND away_team=? AND competition IS ?",
                (stats.match_key[0].isoformat(), stats.match_key[1], stats.match_key[2], stats.match_key[3]),
            ).fetchone()
            if row is None:
                raise KeyError("match for statistics was not found")
            db.execute(
                """INSERT INTO match_stats(match_id,source,xg_home,xg_away,shots_home,shots_away,shots_on_target_home,
                shots_on_target_away,possession_home,possession_away,corners_home,corners_away)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(match_id,source) DO UPDATE SET
                xg_home=excluded.xg_home,xg_away=excluded.xg_away,shots_home=excluded.shots_home,shots_away=excluded.shots_away,
                shots_on_target_home=excluded.shots_on_target_home,shots_on_target_away=excluded.shots_on_target_away,
                possession_home=excluded.possession_home,possession_away=excluded.possession_away,
                corners_home=excluded.corners_home,corners_away=excluded.corners_away""",
                (row[0], stats.source, stats.xg_home, stats.xg_away, stats.shots_home, stats.shots_away,
                 stats.shots_on_target_home, stats.shots_on_target_away, stats.possession_home,
                 stats.possession_away, stats.corners_home, stats.corners_away),
            )

    def upsert_fixture(self, fixture: Fixture) -> None:
        with self._connect() as db:
            db.execute(
                """INSERT INTO fixtures(date,home_team,away_team,refreshed_at)
                VALUES(?,?,?,datetime('now')) ON CONFLICT(date,home_team,away_team)
                DO UPDATE SET refreshed_at=excluded.refreshed_at""",
                (fixture.date.isoformat(), fixture.home_team, fixture.away_team),
            )

    def mark_fixtures_refreshed(self) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM fixtures WHERE date < date('now')")

    def load_fixtures(self, *, from_date: date) -> list[Fixture]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT home_team, away_team, date FROM fixtures WHERE date>=? ORDER BY date, id",
                (from_date.isoformat(),),
            ).fetchall()
        return [Fixture(row[0], row[1], date.fromisoformat(row[2])) for row in rows]

    def count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM matches").fetchone()[0])

    def provenance_count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM provenance").fetchone()[0])

    def stats_count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM match_stats").fetchone()[0])

    def load_matches(self, *, completed_only: bool = True) -> list[Match]:
        query = "SELECT date, home_team, away_team, home_goals, away_goals FROM matches"
        if completed_only:
            query += " WHERE home_goals IS NOT NULL AND away_goals IS NOT NULL"
        query += " ORDER BY date, id"
        with self._connect() as db:
            rows = db.execute(query).fetchall()
        return [Match(date.fromisoformat(row[0]), row[1], row[2], row[3], row[4]) for row in rows]
