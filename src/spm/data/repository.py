"""SQLite persistence for normalized SPM records and provenance."""
import sqlite3
from pathlib import Path

from .normalized import MatchRecord


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
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                home_goals INTEGER,
                away_goals INTEGER,
                competition TEXT,
                season TEXT,
                UNIQUE(date, home_team, away_team, competition)
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS provenance (
                id INTEGER PRIMARY KEY,
                match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
                source TEXT NOT NULL,
                source_id TEXT,
                source_url TEXT,
                retrieved_at TEXT,
                UNIQUE(match_id, source, source_id)
            )""")
            db.execute("CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(date)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_provenance_match ON provenance(match_id)")

    def upsert(self, record: MatchRecord) -> None:
        with self._connect() as db:
            db.execute(
                """INSERT INTO matches(date,home_team,away_team,home_goals,away_goals,competition,season)
                VALUES(?,?,?,?,?,?,?)
                ON CONFLICT(date,home_team,away_team,competition) DO UPDATE SET
                home_goals=COALESCE(excluded.home_goals,matches.home_goals),
                away_goals=COALESCE(excluded.away_goals,matches.away_goals),
                season=COALESCE(excluded.season,matches.season)""",
                (record.date.isoformat(), record.canonical_home_team, record.canonical_away_team,
                 record.home_goals, record.away_goals, record.competition, record.season),
            )
            row = db.execute(
                "SELECT id FROM matches WHERE date=? AND home_team=? AND away_team=? AND competition IS ?",
                (record.date.isoformat(), record.canonical_home_team, record.canonical_away_team, record.competition),
            ).fetchone()
            if row is None:
                raise RuntimeError("failed to locate upserted match")
            match_id = int(row[0])
            for provenance in record.provenance:
                db.execute(
                    """INSERT OR IGNORE INTO provenance(match_id,source,source_id,source_url,retrieved_at)
                    VALUES(?,?,?,?,?)""",
                    (match_id, provenance.source, provenance.source_id, provenance.source_url,
                     provenance.retrieved_at.isoformat() if provenance.retrieved_at else None),
                )

    def count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM matches").fetchone()[0])

    def provenance_count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM provenance").fetchone()[0])
