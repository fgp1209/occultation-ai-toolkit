from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve


def download_sources(urls: list[str], raw_dir: Path) -> list[Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for url in urls:
        try:
            name = Path(urlparse(url).path).name or "downloaded.raw"
            target = raw_dir / name
            urlretrieve(url, target)
            downloaded.append(target)
        except Exception as exc:
            print(f"[WARN] No se pudo descargar {url}: {exc}")
    return downloaded
