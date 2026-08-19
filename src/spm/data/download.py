"""Controlled historical-data downloader.

Network access is intentionally isolated from CSV providers. Downloads are
cached locally and never overwrite an existing file unless explicitly forced.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen


@dataclass(frozen=True, slots=True)
class DownloadResult:
    path: Path
    downloaded: bool
    url: str


def download_cached(url: str, destination: str | Path, *, force: bool = False) -> DownloadResult:
    path = Path(destination)
    if path.exists() and not force:
        return DownloadResult(path, False, url)

    path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "SPM_v2 historical-data-loader"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    if not payload:
        raise ValueError(f"empty download: {url}")
    path.write_bytes(payload)
    return DownloadResult(path, True, url)
