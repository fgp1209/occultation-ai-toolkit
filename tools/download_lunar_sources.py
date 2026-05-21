#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import astropy.units as u
from astropy.coordinates import EarthLocation
from zoneinfo import ZoneInfo

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from occultations.lunar import moon_corridor
from occultations.settings import load_site_settings

GAIA_TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descarga candidatas Gaia DR3 para ocultaciones lunares.")
    parser.add_argument("--settings", default="settings.local.json")
    parser.add_argument("--name")
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lon", type=float)
    parser.add_argument("--alt", type=float)
    parser.add_argument("--timezone")
    parser.add_argument("--from", dest="from_dt", required=True)
    parser.add_argument("--to", dest="to_dt", required=True)
    parser.add_argument("--max-g-mag", type=float, default=11.0)
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
    timezone = ZoneInfo(timezone_name)
    start = datetime.fromisoformat(args.from_dt).astimezone(timezone)
    end = datetime.fromisoformat(args.to_dt).astimezone(timezone)
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt * u.m)
    corridor = moon_corridor(start, end, location)
    query = gaia_query(corridor, args.max_g_mag)
    raw = tap_csv(query)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    diagnostic = {
        "site": {"name": name, "lat": lat, "lon": lon, "alt_m": alt, "timezone": timezone_name},
        "window": {"from_local": start.isoformat(), "to_local": end.isoformat()},
        "source": {"catalog": "Gaia DR3", "tap_sync": GAIA_TAP_SYNC},
        "corridor": corridor,
        "max_g_mag": args.max_g_mag,
        "query": query,
        "candidate_rows": max(0, raw.decode("utf-8", errors="replace").count("\n") - 1),
        "out": str(out),
    }
    diagnostic_path = out.with_suffix(".diagnostic.json")
    diagnostic_path.write_text(json.dumps(diagnostic, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"candidate_rows": diagnostic["candidate_rows"], "out": str(out), "diagnostic": str(diagnostic_path)}, ensure_ascii=False, indent=2))
    return 0


def gaia_query(corridor: dict[str, float], max_g_mag: float) -> str:
    return f"""
SELECT source_id, ra, dec, pmra, pmdec, phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE phot_g_mean_mag <= {max_g_mag}
AND 1 = CONTAINS(
  POINT('ICRS', ra, dec),
  CIRCLE('ICRS', {corridor['ra_deg']}, {corridor['dec_deg']}, {corridor['radius_deg']})
)
""".strip()


def tap_csv(query: str) -> bytes:
    data = urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": query}).encode("utf-8")
    request = Request(GAIA_TAP_SYNC, data=data, headers={"User-Agent": "occultsearch.ai lunar corridor downloader"})
    with urlopen(request, timeout=120) as response:
        return response.read()


if __name__ == "__main__":
    raise SystemExit(main())
