"""Convert validated normalized records into the backtest domain model."""
from __future__ import annotations

from collections.abc import Iterable

from spm.data.models import Match
from spm.data.normalized import MatchRecord
from spm.ingestion.validation import validate_historical_dataset


def to_backtest_matches(records: Iterable[MatchRecord]) -> tuple[Match, ...]:
    """Validate normalized records and convert completed results for backtesting."""
    validated = validate_historical_dataset(records)
    return tuple(
        Match(record.date, record.home_team, record.away_team, record.home_goals, record.away_goals)
        for record in validated
    )
