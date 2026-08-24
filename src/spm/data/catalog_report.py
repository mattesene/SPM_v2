"""Human-readable catalog coverage report."""
from __future__ import annotations

from pathlib import Path

from .coverage import CoverageReport, validate_catalog_coverage
from .default_historical_catalog import default_catalog


def default_coverage_report(root: str | Path) -> CoverageReport:
    return validate_catalog_coverage(default_catalog(), root)


def format_coverage_report(report: CoverageReport) -> str:
    lines = [f"expected={report.expected}", f"present={report.present}", f"complete={report.complete}"]
    if report.missing:
        lines.append("missing:")
        lines.extend(f"- {competition} {season}" for competition, season in report.missing)
    return "\n".join(lines)
