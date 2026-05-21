#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import math

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from occultations.lunar import (
    CALCULATION_LIMITATIONS,
    CALCULATION_NAME,
    detect_lunar_occultations,
    load_gaia_candidates,
    write_lunar_reports,
    candidate_diagnostics,
)
from occultations.settings import load_site_settings
REQUIRED_LOCAL_COLUMNS = {"star_name","catalog","source_id","ra_deg","dec_deg","pmra","pmdec","epoch","mag_v","mag_g"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detecta ocultaciones lunares visibles desde Gaia + Astropy.")
    parser.add_argument("--settings", default="settings.local.json")
    parser.add_argument("--name")
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lon", type=float)
    parser.add_argument("--alt", type=float)
    parser.add_argument("--timezone")
    parser.add_argument("--from", dest="from_dt", required=True)
    parser.add_argument("--to", dest="to_dt", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    site = load_site_settings(Path(args.settings))
    if site is None and any(value is None for value in (args.name, args.lat, args.lon, args.alt, args.timezone)):
        raise SystemExit("Faltan settings locales o sitio completo por CLI.")
    name = args.name or site.name
    lat = args.lat if args.lat is not None else site.lat
    lon = args.lon if args.lon is not None else site.lon
    alt = args.alt if args.alt is not None else site.alt_m
    timezone_name = args.timezone or site.timezone
    tz = ZoneInfo(timezone_name)
    start = datetime.fromisoformat(args.from_dt).astimezone(tz)
    end = datetime.fromisoformat(args.to_dt).astimezone(tz)
    catalog_validation = validate_local_catalog(Path(args.input), start, end, lat, lon, alt)
    candidates = load_gaia_candidates(Path(args.input))
    events = detect_lunar_occultations(candidates, start, end, lat, lon, alt, timezone_name, str(args.input))
    diagnostics = candidate_diagnostics(candidates, start, end, lat, lon, alt, timezone_name, top_n=30)
    payload = {
        "site": {"name": name, "lat": lat, "lon": lon, "alt_m": alt, "timezone": timezone_name},
        "window": {
            "from_local": start.isoformat(),
            "to_local": end.isoformat(),
            "from_utc": start.astimezone(timezone.utc).isoformat(),
            "to_utc": end.astimezone(timezone.utc).isoformat(),
        },
        "source": {
            "catalog": "Gaia DR3 TAP candidate CSV",
            "candidate_file": str(args.input),
            "calculation": CALCULATION_NAME,
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"candidate_stars": len(candidates), "visible_events": len(events)},
        "catalog_validation": catalog_validation,
        "events": events,
        "candidate_diagnostics": diagnostics,
        "limitations": CALCULATION_LIMITATIONS,
    }
    write_lunar_reports(payload, Path(args.out))
    print(json.dumps({"candidate_stars": len(candidates), "visible_events": len(events), "out": args.out, "coverage": catalog_validation}, ensure_ascii=False, indent=2))
    return 0


def validate_local_catalog(path: Path, start: datetime, end: datetime, lat: float, lon: float, alt: float) -> dict:
    import csv
    import astropy.units as u
    from astropy.coordinates import EarthLocation
    from occultations.lunar import moon_corridor

    if not path.exists():
        raise SystemExit(f"Input catalog not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    columns = set(rows[0].keys()) if rows else set()
    missing = sorted(REQUIRED_LOCAL_COLUMNS - columns)
    if missing:
        raise SystemExit(f"Invalid local bright-star catalog; missing columns: {', '.join(missing)}")
    total = len(rows)
    mags = [float(r["mag_v"]) for r in rows if r.get("mag_v") not in ("", None)]
    bright = [m for m in mags if m <= 8.0]
    ras = [float(r["ra_deg"]) for r in rows if r.get("ra_deg")]
    decs = [float(r["dec_deg"]) for r in rows if r.get("dec_deg")]
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt * u.m)
    corridor = moon_corridor(start, end, location)
    stars_within = 0
    bright_within = 0
    for r in rows:
        if not r.get("ra_deg") or not r.get("dec_deg"):
            continue
        sep = _ang_sep_deg(float(r["ra_deg"]), float(r["dec_deg"]), corridor["ra_deg"], corridor["dec_deg"])
        if sep <= corridor["radius_deg"]:
            stars_within += 1
            if r.get("mag_v") not in ("", None) and float(r["mag_v"]) <= 8.0:
                bright_within += 1

    coverage = {
        "total_stars": total,
        "bright_stars_mag_v_le_8": len(bright),
        "ra_range_deg": [min(ras), max(ras)] if ras else None,
        "dec_range_deg": [min(decs), max(decs)] if decs else None,
        "moon_path_ra_min": corridor["ra_deg"] - corridor["radius_deg"],
        "moon_path_ra_max": corridor["ra_deg"] + corridor["radius_deg"],
        "moon_path_dec_min": corridor["dec_deg"] - corridor["radius_deg"],
        "moon_path_dec_max": corridor["dec_deg"] + corridor["radius_deg"],
        "stars_within_corridor": stars_within,
        "bright_stars_within_corridor": bright_within,
        "columns_present": sorted(columns),
    }
    if total < 100 or len(bright) < 20 or bright_within == 0:
        raise SystemExit("Local lunar catalog coverage insufficient for operational validation.")
    return coverage


def _ang_sep_deg(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    r1, d1, r2, d2 = map(math.radians, [ra1, dec1, ra2, dec2])
    cossep = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cossep))))


if __name__ == "__main__":
    raise SystemExit(main())
