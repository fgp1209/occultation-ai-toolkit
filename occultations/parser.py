from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from .config import OccultationEvent
from .xml_parser import parse_iota_xml


KNOWN_COLUMNS = {
    "object_name",
    "object_type",
    "utc_datetime",
    "utc",
    "star_name",
    "star_mag",
    "max_duration_s",
    "mag_drop",
    "ra",
    "dec",
    "source",
    "source_url",
    "source_file",
    "raw_id",
}


def _float(value: str | None) -> float | None:
    return float(value) if value not in {None, ""} else None


def parse_events(path: Path) -> list[OccultationEvent]:
    if not path.exists():
        raise FileNotFoundError(f"No existe input: {path}")
    if path.suffix.lower() == ".xml":
        return parse_iota_xml(path)
    if path.suffix.lower() == ".occelmnt":
        raise NotImplementedError("Formato occelmnt no implementado completamente aun.")

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(2048)
        fh.seek(0)
        delim = "," if sample.count(",") >= sample.count(";") else ";"
        events: list[OccultationEvent] = []
        for raw_row in csv.DictReader(fh, delimiter=delim):
            row = {(key or "").lstrip("\ufeff"): value for key, value in raw_row.items()}
            dt_raw = row.get("utc_datetime") or row.get("utc")
            dt = datetime.fromisoformat(dt_raw).astimezone(timezone.utc) if dt_raw else None
            events.append(
                OccultationEvent(
                    object_name=row.get("object_name"),
                    object_type=row.get("object_type"),
                    utc_datetime=dt,
                    star_name=row.get("star_name"),
                    star_mag=_float(row.get("star_mag")),
                    max_duration_s=_float(row.get("max_duration_s")),
                    mag_drop=_float(row.get("mag_drop")),
                    ra=row.get("ra"),
                    dec=row.get("dec"),
                    source=row.get("source"),
                    source_url=row.get("source_url"),
                    source_file=row.get("source_file") or str(path),
                    raw_id=row.get("raw_id"),
                    raw_line=str(row),
                    extra={key: value for key, value in row.items() if key not in KNOWN_COLUMNS},
                )
            )
        return events
