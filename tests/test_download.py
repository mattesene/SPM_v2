from pathlib import Path

from spm.data.download import download_cached


def test_download_cached_skips_existing_file(tmp_path: Path):
    destination = tmp_path / "season.csv"
    destination.write_text("cached", encoding="utf-8")
    result = download_cached("https://example.invalid/season.csv", destination)
    assert result.downloaded is False
    assert destination.read_text(encoding="utf-8") == "cached"
