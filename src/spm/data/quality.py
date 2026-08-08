"""Data-quality checks applied before records enter the model."""
from dataclasses import dataclass
from datetime import date

from .normalized import MatchRecord


@dataclass(frozen=True, slots=True)
class QualityIssue:
    code: str
    message: str
    record_index: int


def validate_records(records: list[MatchRecord], *, as_of: date | None = None) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    seen: dict[tuple, int] = {}
    for index, record in enumerate(records):
        if as_of is not None and record.date > as_of:
            issues.append(QualityIssue("future_record", "record is after the analysis date", index))
        if record.home_team.strip() == record.away_team.strip():
            issues.append(QualityIssue("same_team", "home and away teams are identical", index))
        if (record.home_goals is None) != (record.away_goals is None):
            issues.append(QualityIssue("partial_score", "score is partially populated", index))
        key = record.identity_key
        if key in seen:
            issues.append(QualityIssue("duplicate_identity", f"duplicate of record {seen[key]}", index))
        else:
            seen[key] = index
    return issues
