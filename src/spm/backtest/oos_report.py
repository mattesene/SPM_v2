"""Stable, machine-readable OOS report generation."""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .oos_aggregation import OOSAggregate


def aggregate_to_dict(summary: OOSAggregate) -> dict[str, object]:
    return asdict(summary)


def write_oos_report(summary: OOSAggregate, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(aggregate_to_dict(summary), indent=2, sort_keys=True), encoding="utf-8")
