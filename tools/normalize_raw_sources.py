#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import zipfile
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from occultations.config import OccultationEvent
from occultations.parser import parse_events
from occultations.raw_sources import parse_call4obs_html
from occultations.xml_parser import PARSER_VERSION, parse_iota_xml

FIELDNAMES = [
    "object_name",
    "object_type",
    "utc_datetime",
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
]
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normaliza raw reales de ocultaciones a CSV interno.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--from", dest="from_dt", required=True)
    parser.add_argument("--to", dest="to_dt", required=True)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(argv)


def normalize_raw_sources(
    raw_dir: Path,
    start: datetime,
    end: datetime,
    timezone_name: str,
    out: Path,
) -> dict:
    sources = supported_files(raw_dir)
    key = cache_key(raw_dir, sources, start, end, timezone_name)
    diagnostic_path = out.with_suffix(".diagnostic.json")
    cache_path = out.with_suffix(".cache.json")
    if cache_matches(out, cache_path, key):
        diagnostic = json.loads(diagnostic_path.read_text(encoding="utf-8"))
        diagnostic["cache"] = "hit"
        diagnostic_path.write_text(json.dumps(diagnostic, ensure_ascii=False, indent=2), encoding="utf-8")
        return diagnostic

    diagnostic = {
        "cache": "miss",
        "parser_version": PARSER_VERSION,
        "raw_dir": str(raw_dir),
        "from_local": start.isoformat(),
        "to_local": end.isoformat(),
        "timezone": timezone_name,
        "files_read": [],
        "total_files_read": 0,
        "total_events_parsed": 0,
        "total_events_normalized": 0,
        "events_in_week_window": 0,
        "events_in_30d_window": 0,
        "events_passed_to_scorer": 0,
        "discarded": [],
        "discarded_by_reason": {},
        "events_discarded_by_format": 0,
        "errors_by_file": {},
        "unrecognized_fields": ["xml.Object max duration slot", "xml.Errors uncertainty mapping"],
    }
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()
    week_end = min(end, start + timedelta(days=7) - timedelta(seconds=1))
    for source in sources:
        record = {"file": str(source), "events_found": 0, "events_in_window": 0, "format": source.suffix.lower()}
        diagnostic["files_read"].append(record)
        diagnostic["total_files_read"] += 1
        try:
            events = list(read_source(source))
        except Exception as exc:
            diagnostic["errors_by_file"][str(source)] = str(exc)
            continue
        record["events_found"] = len(events)
        diagnostic["total_events_parsed"] += len(events)
        for event in events:
            reason = required_reason(event)
            if reason:
                diagnostic["events_discarded_by_format"] += 1
                keep_discard(diagnostic, event, reason)
                continue
            if start <= event.utc_datetime.astimezone(start.tzinfo) <= week_end:
                diagnostic["events_in_week_window"] += 1
            if start <= event.utc_datetime.astimezone(start.tzinfo) <= end:
                diagnostic["events_in_30d_window"] += 1
                record["events_in_window"] += 1
            else:
                keep_discard(diagnostic, event, "fuera de ventana")
                continue
            row = as_row(event)
            dedupe = (row["utc_datetime"], row["object_name"], row["star_name"], row["raw_id"])
            if dedupe in seen:
                keep_discard(diagnostic, event, "duplicado")
                continue
            seen.add(dedupe)
            rows.append(row)

    rows.sort(key=lambda row: row["utc_datetime"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    diagnostic["total_events_normalized"] = len(rows)
    diagnostic["events_passed_to_scorer"] = len(rows)
    diagnostic_path.write_text(json.dumps(diagnostic, ensure_ascii=False, indent=2), encoding="utf-8")
    cache_path.write_text(json.dumps({"key": key}, ensure_ascii=False, indent=2), encoding="utf-8")
    return diagnostic


def supported_files(raw_dir: Path) -> list[Path]:
    files = [
        path
        for path in raw_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".xml", ".csv", ".html", ".zip"}
    ]
    return sorted(path for path in files if path.suffix.lower() != ".zip" or not extracted_xml_exists(path))


def extracted_xml_exists(zip_path: Path) -> bool:
    stem = zip_path.stem
    if stem.endswith("-iota"):
        extracted_dir = zip_path.parent / "iota"
    elif stem.endswith("-raw-generic"):
        extracted_dir = zip_path.parent / "raw-generic"
    elif stem.endswith("-raw-priority"):
        extracted_dir = zip_path.parent / "raw-priority"
    else:
        return False
    return any(extracted_dir.rglob("*.xml")) if extracted_dir.exists() else False


def read_source(path: Path) -> Iterable[OccultationEvent]:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return parse_call4obs_html(path)
    if suffix == ".zip":
        return read_zip_xml(path)
    return parse_events(path)


def read_zip_xml(path: Path) -> list[OccultationEvent]:
    events: list[OccultationEvent] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.filename.lower().endswith(".xml"):
                virtual_path = Path(f"{path}!{info.filename}")
                events.extend(parse_iota_xml(virtual_path, archive.read(info)))
    return events


def required_reason(event: OccultationEvent) -> str | None:
    if event.utc_datetime is None:
        return "fecha UTC no parseable"
    if not event.object_name:
        return "objeto no parseable"
    if not event.star_name:
        return "estrella no parseable"
    return None


def keep_discard(diagnostic: dict, event: OccultationEvent, reason: str) -> None:
    diagnostic["discarded_by_reason"][reason] = diagnostic["discarded_by_reason"].get(reason, 0) + 1
    if len(diagnostic["discarded"]) < 500:
        diagnostic["discarded"].append(
            {
                "event": event.object_name,
                "utc_datetime": event.utc_datetime.isoformat() if event.utc_datetime else None,
                "source_file": event.source_file,
                "raw_id": event.raw_id,
                "reason": reason,
            }
        )


def as_row(event: OccultationEvent) -> dict[str, str]:
    data = asdict(event)
    row = {name: "" if data.get(name) is None else str(data.get(name)) for name in FIELDNAMES}
    row["utc_datetime"] = event.utc_datetime.astimezone(timezone.utc).isoformat() if event.utc_datetime else ""
    return row


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_key(raw_dir: Path, sources: list[Path], start: datetime, end: datetime, timezone_name: str) -> dict:
    return {
        "raw_dir": str(raw_dir.resolve()),
        "files": [{"path": str(path.relative_to(raw_dir)), "sha256": file_hash(path)} for path in sources],
        "from": start.isoformat(),
        "to": end.isoformat(),
        "timezone": timezone_name,
        "parser_version": PARSER_VERSION,
    }


def cache_matches(out: Path, cache_path: Path, key: dict) -> bool:
    if not out.exists() or not cache_path.exists() or not out.with_suffix(".diagnostic.json").exists():
        return False
    try:
        return json.loads(cache_path.read_text(encoding="utf-8")).get("key") == key
    except json.JSONDecodeError:
        return False


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    tz = ZoneInfo(args.timezone)
    start = datetime.fromisoformat(args.from_dt).astimezone(tz)
    end = datetime.fromisoformat(args.to_dt).astimezone(tz)
    if end < start:
        raise SystemExit("--to debe ser posterior a --from")
    diagnostic = normalize_raw_sources(Path(args.raw_dir), start, end, args.timezone, Path(args.out))
    summary = {
        "cache": diagnostic["cache"],
        "files_read": diagnostic["total_files_read"],
        "events_parsed": diagnostic["total_events_parsed"],
        "events_in_week_window": diagnostic["events_in_week_window"],
        "events_in_30d_window": diagnostic["events_in_30d_window"],
        "events_passed_to_scorer": diagnostic["events_passed_to_scorer"],
        "normalized_csv": args.out,
        "diagnostic_json": str(Path(args.out).with_suffix(".diagnostic.json")),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
