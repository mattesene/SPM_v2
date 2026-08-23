from datetime import date

from spm.live.providers import CSVFixtureProvider


def test_csv_fixture_provider_filters_by_date(tmp_path):
    source = tmp_path / "fixtures.csv"
    source.write_text(
        "home,away,kickoff\nOld,Team,2026-08-22\nTeam A,Team B,2026-08-24\n",
        encoding="utf-8",
    )
    fixtures = CSVFixtureProvider(source).fetch_fixtures(date(2026, 8, 23))
    assert len(fixtures) == 1
    assert fixtures[0].home == "Team A"
    assert fixtures[0].away == "Team B"
