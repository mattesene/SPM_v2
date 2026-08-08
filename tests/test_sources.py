from spm.data.sources import DataRole, sources_for


def test_results_have_multiple_independent_sources() -> None:
    sources = sources_for(DataRole.RESULTS)
    names = {source.name for source in sources}
    assert {"Diretta.it", "Sofascore", "FBref"} <= names


def test_whoscored_is_not_marked_as_primary_results_source() -> None:
    names = {source.name for source in sources_for(DataRole.RESULTS)}
    assert "WhoScored" not in names
