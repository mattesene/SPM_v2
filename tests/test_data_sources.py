from datetime import date

from spm.data.normalized import MatchRecord
from spm.data.provenance import Provenance
from spm.data.repository import MatchRepository
from spm.data.sources import DataRole, sources_for


def test_source_registry_has_results_sources() -> None:
    sources = sources_for(DataRole.RESULTS)
    assert any(source.name == "Diretta.it" for source in sources)
    assert any(source.name == "Sofascore" for source in sources)


def test_match_record_provenance_and_sqlite(tmp_path) -> None:
    record = MatchRecord(
        date(2026, 8, 8), "Inter", "Milan", 2, 1,
        competition="Serie A", season="2026/27",
        provenance=(Provenance("sofascore", "match-1"), Provenance("fbref", "match-1")),
    )
    assert record.completed
    assert record.source_count == 2
    repo = MatchRepository(tmp_path / "spm.db")
    repo.upsert(record)
    assert repo.count() == 1
    repo.upsert(record)
    assert repo.count() == 1
