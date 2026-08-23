"""Validate and describe the Live data inputs before production refresh."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LiveDataManifest:
    database: Path
    oos: Path

    def validate(self) -> None:
        for path, label in ((self.database, "database"), (self.oos, "OOS file")):
            if not path.is_file():
                raise FileNotFoundError(f"Live {label} not found: {path}")
            if path.stat().st_size == 0:
                raise ValueError(f"Live {label} is empty: {path}")


def validate_live_inputs(database: str | Path, oos: str | Path) -> LiveDataManifest:
    manifest = LiveDataManifest(Path(database), Path(oos))
    manifest.validate()
    return manifest
