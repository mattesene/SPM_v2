"""Chronological train/validation/OOS splitting utilities."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Sequence


@dataclass(frozen=True, slots=True)
class TemporalSplit:
    train: tuple
    validation: tuple
    oos: tuple


def temporal_split(items: Sequence, *, train_end: date, validation_end: date) -> TemporalSplit:
    if train_end >= validation_end:
        raise ValueError("train_end must be before validation_end")
    train, validation, oos = [], [], []
    for item in items:
        d = item.match_date if hasattr(item, "match_date") else item.date
        if d <= train_end:
            train.append(item)
        elif d <= validation_end:
            validation.append(item)
        else:
            oos.append(item)
    if not train or not validation or not oos:
        raise ValueError("temporal split must contain train, validation and OOS data")
    return TemporalSplit(tuple(train), tuple(validation), tuple(oos))
