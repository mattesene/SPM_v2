from spm.data.historical_catalog import build_catalog


def test_build_catalog_creates_cartesian_competition_season_set():
    catalog = build_catalog(["E0", "I1"], ["2324", "2425"])
    assert len(catalog.sources) == 4
    assert {source.competition for source in catalog.sources} == {"e0", "i1"}
