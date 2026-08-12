from pathlib import Path

from spm.data.providers.football_data import FootballDataCSVProvider


def test_football_data_provider_normalizes_standard_csv(tmp_path: Path):
    csv_path = tmp_path / "ITA1.csv"
    csv_path.write_text(
        "Date,HomeTeam,AwayTeam,FTHG,FTAG\n01/08/26,Inter,Juventus,2,1\n",
        encoding="utf-8",
    )

    records = FootballDataCSVProvider("Serie A", "2026/27").load(csv_path)

    assert len(records) == 1
    record = records[0]
    assert record.competition == "Serie A"
    assert record.season == "2026/27"
    assert record.home_goals == 2
    assert record.away_goals == 1
    assert record.provenance[0].source == "football-data.co.uk"
    assert record.provenance[0].source_id == "ITA1.csv:2"
