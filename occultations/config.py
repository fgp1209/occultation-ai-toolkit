from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class SiteConfig:
    name: str
    lat: float
    lon: float
    alt_m: float
    timezone: str


DEFAULT_SITE = SiteConfig(
    name="Observatori de Sabadell",
    lat=41.550111,
    lon=2.091453,
    alt_m=224,
    timezone="Europe/Madrid",
)


@dataclass(slots=True)
class OccultationEvent:
    object_name: str | None = None
    object_type: str | None = None
    utc_datetime: datetime | None = None
    star_name: str | None = None
    star_mag: float | None = None
    max_duration_s: float | None = None
    mag_drop: float | None = None
    ra: str | None = None
    dec: str | None = None
    source: str | None = None
    source_url: str | None = None
    source_file: str | None = None
    raw_id: str | None = None
    raw_line: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunConfig:
    site: SiteConfig
    from_dt: datetime
    to_dt: datetime
    horizon_days: int = 30
    max_mag: float = 11
    min_alt: float = 20
    min_duration: float = 0
    include_subsecond: bool = True
    input_path: Path | None = None
    raw_dir: Path = Path("data/raw")
    download: bool = False
    out: Path = Path("reports/output")
    source_urls: list[str] = field(default_factory=list)
