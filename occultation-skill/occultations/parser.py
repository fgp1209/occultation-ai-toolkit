from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from .config import OccultationEvent


def parse_events(path: Path) -> list[OccultationEvent]:
    if not path.exists():
        raise FileNotFoundError(f"No existe input: {path}")
    if path.suffix.lower() == ".occelmnt":
        raise NotImplementedError("Formato occelmnt no implementado completamente aún.")
    with path.open("r", encoding="utf-8") as fh:
        sample = fh.read(2048)
        fh.seek(0)
        delim = "," if sample.count(",") >= sample.count(";") else ";"
        reader = csv.DictReader(fh, delimiter=delim)
        events: list[OccultationEvent] = []
        for row in reader:
            dt_raw = row.get("utc_datetime") or row.get("utc")
            dt = datetime.fromisoformat(dt_raw).astimezone(timezone.utc) if dt_raw else None
            events.append(
                OccultationEvent(
                    object_name=row.get("object_name"),
                    object_type=row.get("object_type"),
                    utc_datetime=dt,
                    star_name=row.get("star_name"),
                    star_mag=float(row["star_mag"]) if row.get("star_mag") else None,
                    max_duration_s=float(row["max_duration_s"]) if row.get("max_duration_s") else None,
                    mag_drop=float(row["mag_drop"]) if row.get("mag_drop") else None,
                    ra=row.get("ra"),
                    dec=row.get("dec"),
                    source_file=str(path),
                    raw_line=str(row),
                    extra={k: v for k, v in row.items() if k not in {"object_name","object_type","utc_datetime","utc","star_name","star_mag","max_duration_s","mag_drop","ra","dec"}},
                )
            )
        return events
