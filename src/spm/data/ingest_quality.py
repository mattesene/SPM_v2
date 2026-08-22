"""Quality gate for canonical match ingestion."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from .normalized import MatchRecord
from .quality import QualityIssue, validate_records


@dataclass(frozen=True, slots=True)
class QualityGateResult:
    accepted: tuple[MatchRecord, ...]
    rejected: tuple[MatchRecord, ...]
    issues: tuple[QualityIssue, ...]


def apply_quality_gate(records: Iterable[MatchRecord], *, as_of: date | None = None) -> QualityGateResult:
    rows = tuple(records)
    issues = tuple(validate_records(list(rows), as_of=as_of))
    rejected_indexes = {issue.record_index for issue in issues}
    return QualityGateResult(
        tuple(row for i, row in enumerate(rows) if i not in rejected_indexes),
        tuple(row for i, row in enumerate(rows) if i in rejected_indexes),
        issues,
    )
