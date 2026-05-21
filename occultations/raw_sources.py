from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

from .config import OccultationEvent

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _plain_text(raw: str) -> str:
    raw = html.unescape(raw)
    raw = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.I | re.S)
    raw = re.sub(r"<style\b.*?</style>", " ", raw, flags=re.I | re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def parse_call4obs_html(path: Path) -> list[OccultationEvent]:
    text = _plain_text(path.read_text(encoding="utf-8", errors="replace"))
    rx = re.compile(
        r"(?P<year>20\d{2})\s+"
        r"(?P<month>[A-Za-z]+)\s+"
        r"(?P<day>\d{1,2})\s+"
        r"~(?P<hour>\d{2}):(?P<minute>\d{2})\s+UT:\s+"
        r"\((?P<number>[^)]+)\)\s+"
        r"(?P<name>.*?)\s+occults\s+"
        r"(?P<star>.*?)\s+"
        r"\((?P<mag>\d+(?:\.\d+)?)\s+mag\)",
        flags=re.I,
    )
    events: list[OccultationEvent] = []
    seen: set[tuple[str, str, str]] = set()
    for match in rx.finditer(text):
        month = MONTHS.get(match.group("month").lower()[:3])
        if month is None:
            continue
        dt = datetime(
            int(match.group("year")),
            month,
            int(match.group("day")),
            int(match.group("hour")),
            int(match.group("minute")),
            tzinfo=timezone.utc,
        )
        object_name = f"({match.group('number').strip()}) {match.group('name').strip()}"
        star_name = match.group("star").strip()
        key = (dt.isoformat(), object_name, star_name)
        if key in seen:
            continue
        seen.add(key)
        context = text[max(0, match.start() - 500) : min(len(text), match.end() + 900)]
        duration = re.search(
            r"(?:max\.\s*)?duration(?:\s+of)?(?:\s+only)?\s+(\d+(?:\.\d+)?)\s*s",
            context,
            flags=re.I,
        )
        events.append(
            OccultationEvent(
                object_name=object_name,
                object_type=_object_type(context),
                utc_datetime=dt,
                star_name=star_name,
                star_mag=float(match.group("mag")),
                max_duration_s=float(duration.group(1)) if duration else None,
                source="call4obs",
                source_url="https://call4obs.iota-es.de/",
                source_file=str(path),
                extra={"html_context": context},
            )
        )
    return events


def _object_type(context: str) -> str:
    lower = context.lower()
    if "cubewano" in lower:
        return "cubewano"
    if "centaur" in lower:
        return "centaur"
    if "dwarf planet" in lower:
        return "dwarf_planet"
    if "tno" in lower or "trans-neptun" in lower:
        return "tno"
    if "across" in lower:
        return "across"
    if "nea" in lower or "near earth" in lower:
        return "nea"
    return "mba"
