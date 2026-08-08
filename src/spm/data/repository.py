"""SQLite persistence for normalized SPM records."""
import sqlite3
from pathlib import Path

from .normalized import MatchRecord

class MatchRepository:
    def __init__(self, path: str | Path = "spm.db") -> None:
        self.path = str(path)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY, date TEXT NOT NULL, home_team TEXT NOT NULL,
                away_team TEXT NOT NULL, home_goals INTEGER, away_goals INTEGER,
                competition TEXT, season TEXT, UNIQUE(date, home_team, away_team, competition)
            )""")
            db.execute("CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(date)")

    def upsert(self, record: MatchRecord) -> None:
        with self._connect() as db:
            db.execute("""INSERT INTO matches(date,home_team,away_team,home_goals,away_goals,competition,season)
                VALUES(?,?,?,?,?,?,?) ON CONFLICT(date,home_team,away_team,competition)
                DO UPDATE SET home_goals=excluded.home_goals, away_goals=excluded.away_goals,
                season=COALESCE(excluded.season,matches.season)""",
                (record.date.isoformat(), record.home_team, record.away_team, record.home_goals,
                 record.away_goals, record.competition, record.season))

    def count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM matches").fetchone()[0])
