#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from occultations.lunar import (
    CALCULATION_LIMITATIONS,
    CALCULATION_NAME,
    detect_lunar_occultations,
    load_gaia_candidates,
    write_lunar_reports,
)
from occultations.settings import load_site_settings


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
    candidates = load_gaia_candidates(Path(args.input))
    events = detect_lunar_occultations(candidates, start, end, lat, lon, alt, timezone_name, str(args.input))
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
        "events": events,
        "limitations": CALCULATION_LIMITATIONS,
    }
    write_lunar_reports(payload, Path(args.out))
    print(json.dumps({"candidate_stars": len(candidates), "visible_events": len(events), "out": args.out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
