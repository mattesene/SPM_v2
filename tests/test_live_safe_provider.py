from datetime import date

from spm.live.safe_provider import safe_fetch


class BrokenProvider:
    def fetch_fixtures(self, from_date):
        raise RuntimeError("source unavailable")


def test_safe_fetch_converts_provider_failure_to_result():
    result = safe_fetch(BrokenProvider(), date(2026, 8, 23))
    assert result.source_ok is False
    assert result.fixtures == []
    assert "source unavailable" in result.error
