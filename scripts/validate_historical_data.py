"""Validate the complete default historical dataset scope and emit JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from spm.data.historical_pipeline import prepare_historical_scope
from spm.data.historical_scope import default_historical_scope


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".historical-cache"))
    parser.add_argument("--output", type=Path, default=Path("reports/historical_data_validation.json"))
    args = parser.parse_args()

    scope = default_historical_scope(args.root)
    result = prepare_historical_scope(scope)
    payload = {
        "expected_datasets": len(scope.catalog.sources),
        "downloaded_or_cached": len(result.downloads),
        "missing_datasets": len(result.missing),
        "complete": result.complete,
        "missing": [str(path) for path in result.missing],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if result.complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
