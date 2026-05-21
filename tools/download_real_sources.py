#!/usr/bin/env python3
"""
download_real_sources.py

Downloader/normalizador real para occultsearch.ai.

Fuentes:
- Call4Obs IOTA/ES: eventos publicados en portada.
- Lucky Star: índices + páginas occ.php con circunstancias reales.
- Steve Preston / asteroidoccultation.com: ZIPs .occelmnt para raw local.

Salida principal compatible con occultations/parser.py:
object_name,object_type,utc_datetime,star_name,star_mag,max_duration_s,mag_drop,ra,dec

Uso:
python tools/download_real_sources.py \
  --from "2026-05-24T19:00:00+00:00" \
  --to   "2026-05-25T05:00:00+00:00" \
  --out data/raw/real_occultations_2026-05-24_25.csv \
  --download-preston-zips

Luego:
python occultations/run.py \
  --name "Observatori de Sabadell" \
  --lat 41.548 --lon 2.107 --alt 220 \
  --timezone Europe/Madrid \
  --from "2026-05-24T21:00:00+02:00" \
  --to "2026-05-25T07:00:00+02:00" \
  --input data/raw/real_occultations_2026-05-24_25.csv \
  --out reports/sabadell-2026-05-24-night
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin
from urllib.request import Request, urlopen


CALL4OBS_URL = "https://call4obs.iota-es.de/"
LUCKYSTAR_INDEXES = [
    "https://lesia.obspm.fr/lucky-star/predictions.php",
    "https://lesia.obspm.fr/lucky-star/predp0.php",
]
PRESTON_ZIPS = {
    "iota": "https://asteroidoccultation.com/{year}/{year}-iota.zip",
    "raw-generic": "https://asteroidoccultation.com/{year}/{year}-raw-generic.zip",
    "raw-priority": "https://asteroidoccultation.com/{year}/{year}-raw-priority.zip",
}

MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

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
]


@dataclass(frozen=True)
class Event:
    object_name: str = ""
    object_type: str = ""
    utc_datetime: str = ""
    star_name: str = ""
    star_mag: str = ""
    max_duration_s: str = ""
    mag_drop: str = ""
    ra: str = ""
    dec: str = ""
    source: str = ""
    source_url: str = ""


def http_get(url: str, timeout: int = 45) -> bytes:
    req = Request(
        url,
        headers={
            "User-Agent": "occultsearch.ai/0.1 (+local research downloader)",
            "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,*/*",
        },
    )
    with urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_text(url: str) -> str:
    raw = http_get(url)
    return raw.decode("utf-8", errors="replace")


def clean_text(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"<script\b.*?</script>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_iso(dt: str | None) -> datetime | None:
    if not dt:
        return None
    return datetime.fromisoformat(dt.replace("Z", "+00:00")).astimezone(timezone.utc)


def in_window(event: Event, start: datetime | None, end: datetime | None) -> bool:
    if not event.utc_datetime:
        return False
    try:
        dt = parse_iso(event.utc_datetime)
    except Exception:
        return False
    if dt is None:
        return False
    if start and dt < start:
        return False
    if end and dt > end:
        return False
    return True


def parse_float(raw: str | None) -> str:
    if not raw:
        return ""
    m = re.search(r"[-+]?\d+(?:\.\d+)?", raw.replace(",", "."))
    return m.group(0) if m else ""


def object_type_from_context(ctx: str) -> str:
    c = ctx.lower()
    if any(x in c for x in ["trans-neptunian", "transneptunian", "tno", "cubewano", "dwarf planet", "haumea", "quaoar", "makemake", "orcus", "varuna"]):
        return "tno"
    if "centaur" in c:
        return "centaur"
    if "trojan" in c:
        return "trojan"
    if any(x in c for x in ["near earth", "nea", "amor", "apollo", "aten", "across"]):
        return "nea"
    if any(x in c for x in ["main-belt", "main belt", "mba"]):
        return "mba"
    return ""


def parse_call4obs(html_text: str) -> list[Event]:
    text = clean_text(html_text)
    events: list[Event] = []
    seen: set[tuple[str, str, str]] = set()

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

    for m in rx.finditer(text):
        year = int(m.group("year"))
        month = MONTHS[m.group("month").lower()[:3]]
        day = int(m.group("day"))
        hour = int(m.group("hour"))
        minute = int(m.group("minute"))
        dt = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

        obj = f"({m.group('number').strip()}) {m.group('name').strip()}"
        star = m.group("star").strip()
        key = (dt.isoformat(), obj, star)
        if key in seen:
            continue
        seen.add(key)

        ctx = text[max(0, m.start() - 500): min(len(text), m.end() + 900)]
        duration = ""
        dur_match = re.search(
            r"(?:max\.\s*)?duration(?:\s+of)?(?:\s+only)?\s+(\d+(?:\.\d+)?)\s*s",
            ctx,
            flags=re.I,
        )
        if dur_match:
            duration = dur_match.group(1)

        owc = ""
        owc_match = re.search(r"https://cloud\.occultwatcher\.net/event/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+", ctx)
        if owc_match:
            owc = owc_match.group(0)

        events.append(
            Event(
                object_name=obj,
                object_type=object_type_from_context(ctx),
                utc_datetime=dt.isoformat(),
                star_name=star,
                star_mag=m.group("mag"),
                max_duration_s=duration,
                mag_drop="",
                ra="",
                dec="",
                source="call4obs",
                source_url=owc or CALL4OBS_URL,
            )
        )

    return events


def find_luckystar_detail_urls(index_html: str, base_url: str) -> list[str]:
    urls = set()
    for href in re.findall(r'href=["\']([^"\']*occ\.php\?p=\d+[^"\']*)["\']', index_html, flags=re.I):
        urls.add(urljoin(base_url, html.unescape(href)))
    for href in re.findall(r"(?:https?://[^\s\"']+)?/lucky-star/occ\.php\?p=\d+", index_html, flags=re.I):
        urls.add(urljoin(base_url, html.unescape(href)))
    return sorted(urls)


def hms_to_ra(raw: str) -> str:
    parts = raw.strip().split()
    return ":".join(parts[:3]) if len(parts) >= 3 else raw.strip()


def dms_to_dec(raw: str) -> str:
    parts = raw.strip().split()
    return ":".join(parts[:3]) if len(parts) >= 3 else raw.strip()


def parse_luckystar_detail(page: str, url: str) -> Event | None:
    text = clean_text(page)

    title = re.search(r"Occultation by\s+(.+?)\s+\((20\d{2}-\d{2}-\d{2})\)", text, flags=re.I)
    object_name = title.group(1).strip() if title else ""

    dt_match = re.search(
        r"Date\s+[A-Za-z]{2,4}\.?\s+(\d{1,2})\s+([A-Za-z]+)\.?\s+(20\d{2})\s+(\d{2}:\d{2}:\d{2})",
        text,
        flags=re.I,
    )
    if not dt_match:
        return None

    day = int(dt_match.group(1))
    month = MONTHS[dt_match.group(2).lower()[:3]]
    year = int(dt_match.group(3))
    hh, mm, ss = [int(x) for x in dt_match.group(4).split(":")]
    dt = datetime(year, month, day, hh, mm, ss, tzinfo=timezone.utc)

    pos_match = re.search(
        r"Star position \(ICRF\)\s+(\d{1,2}\s+\d{1,2}\s+\d+(?:\.\d+)?)\s+([+-]\d{1,2}\s+\d{1,2}\s+\d+(?:\.\d+)?)",
        text,
        flags=re.I,
    )
    ra = hms_to_ra(pos_match.group(1)) if pos_match else ""
    dec = dms_to_dec(pos_match.group(2)) if pos_match else ""

    source_id = re.search(r"Star source ID\s+(\d+)", text, flags=re.I)
    catalogue = re.search(r"Stellar catalogue\s+([A-Za-z0-9 _.-]+?)\s+Star astrometric", text, flags=re.I)
    star_name = ""
    if catalogue or source_id:
        star_name = f"{catalogue.group(1).strip() if catalogue else 'Gaia'} {source_id.group(1) if source_id else ''}".strip()

    gmag = re.search(r"\bG magnitude\s+(\d+(?:\.\d+)?)", text, flags=re.I)
    gmag_star = re.search(r"\bG mag\*\s+(\d+(?:\.\d+)?)", text, flags=re.I)
    star_mag = (gmag.group(1) if gmag else gmag_star.group(1) if gmag_star else "")

    drop = parse_float((re.search(r"Magnitude drop\s+([-+]?\d+(?:\.\d+)?)", text, flags=re.I) or [None, ""])[1])
    duration = parse_float((re.search(r"Maximum duration\s+([-+]?\d+(?:\.\d+)?)\s*sec", text, flags=re.I) or [None, ""])[1])

    dyn = re.search(r"Dynamic class\(1\)\s+([A-Za-z0-9 _.-]+?)\s+Semi major axis", text, flags=re.I)
    otype = object_type_from_context(dyn.group(1) if dyn else object_name)

    return Event(
        object_name=object_name,
        object_type=otype,
        utc_datetime=dt.isoformat(),
        star_name=star_name,
        star_mag=star_mag,
        max_duration_s=duration,
        mag_drop=drop,
        ra=ra,
        dec=dec,
        source="luckystar",
        source_url=url,
    )


def download_luckystar(max_details: int = 200) -> list[Event]:
    detail_urls: list[str] = []
    for idx in LUCKYSTAR_INDEXES:
        try:
            html_text = fetch_text(idx)
        except Exception as exc:
            print(f"[WARN] Lucky Star index failed: {idx}: {exc}", file=sys.stderr)
            continue
        detail_urls.extend(find_luckystar_detail_urls(html_text, idx))

    deduped = sorted(set(detail_urls))[:max_details]
    events: list[Event] = []

    for url in deduped:
        try:
            page = fetch_text(url)
            evt = parse_luckystar_detail(page, url)
            if evt:
                events.append(evt)
        except Exception as exc:
            print(f"[WARN] Lucky Star detail failed: {url}: {exc}", file=sys.stderr)

    return events


def download_preston_zips(year: int, raw_dir: Path) -> list[Path]:
    out_dir = raw_dir / "preston" / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    for name, template in PRESTON_ZIPS.items():
        url = template.format(year=year)
        target = out_dir / f"{year}-{name}.zip"
        try:
            target.write_bytes(http_get(url, timeout=120))
            saved.append(target)

            extract_dir = out_dir / name
            extract_dir.mkdir(parents=True, exist_ok=True)
            try:
                with zipfile.ZipFile(target) as zf:
                    zf.extractall(extract_dir)
            except zipfile.BadZipFile:
                print(f"[WARN] ZIP inválido/no extraíble: {target}", file=sys.stderr)

        except Exception as exc:
            print(f"[WARN] Preston ZIP failed: {url}: {exc}", file=sys.stderr)

    return saved


def write_csv(events: Iterable[Event], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    seen = set()

    for e in events:
        key = (e.utc_datetime, e.object_name, e.star_name, e.source)
        if key in seen:
            continue
        seen.add(key)
        rows.append(asdict(e))

    rows.sort(key=lambda r: r.get("utc_datetime") or "")

    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Descarga y normaliza fuentes reales de ocultaciones.")
    p.add_argument("--from", dest="from_dt", help="Inicio UTC/local ISO. Ej: 2026-05-24T19:00:00+00:00")
    p.add_argument("--to", dest="to_dt", help="Fin UTC/local ISO. Ej: 2026-05-25T05:00:00+00:00")
    p.add_argument("--out", default="data/raw/real_occultations.csv")
    p.add_argument("--raw-dir", default="data/raw")
    p.add_argument("--year", type=int, default=datetime.now(timezone.utc).year)
    p.add_argument("--skip-call4obs", action="store_true")
    p.add_argument("--skip-luckystar", action="store_true")
    p.add_argument("--download-preston-zips", action="store_true")
    p.add_argument("--luckystar-max-details", type=int, default=200)
    args = p.parse_args(argv)

    start = parse_iso(args.from_dt)
    end = parse_iso(args.to_dt)
    raw_dir = Path(args.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    events: list[Event] = []

    if not args.skip_call4obs:
        html_text = fetch_text(CALL4OBS_URL)
        (raw_dir / "call4obs_home.html").write_text(html_text, encoding="utf-8")
        events.extend(parse_call4obs(html_text))

    if not args.skip_luckystar:
        events.extend(download_luckystar(max_details=args.luckystar_max_details))

    if args.download_preston_zips:
        download_preston_zips(args.year, raw_dir)

    if start or end:
        events = [e for e in events if in_window(e, start, end)]

    out = Path(args.out)
    write_csv(events, out)

    print(f"[OK] eventos normalizados: {len(events)}")
    print(f"[OK] CSV: {out}")
    if args.download_preston_zips:
        print(f"[OK] ZIPs Preston en: {raw_dir / 'preston' / str(args.year)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
