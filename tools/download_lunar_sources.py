#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import astropy.units as u
from astropy.coordinates import EarthLocation

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from occultations.lunar import moon_corridor
from occultations.settings import load_site_settings
from tools.run_lunar_occultations import validate_local_catalog

GAIA_TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"
LOCAL_BRIGHT_CATALOG = Path("data/raw/lunar/bright-stars.csv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
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


def tap_or_local_bright_csv(query: str) -> tuple[bytes, str]:
    data = urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": query}).encode("utf-8")
    request = Request(GAIA_TAP_SYNC, data=data, headers={"User-Agent": "occultsearch.ai lunar downloader"})
    try:
        with urlopen(request, timeout=120) as response:
            return response.read(), "gaia_tap_live"
    except HTTPError as err:
        if err.code != 403:
            raise
    except Exception:
        pass
    if LOCAL_BRIGHT_CATALOG.exists() and LOCAL_BRIGHT_CATALOG.stat().st_size > 0:
        return LOCAL_BRIGHT_CATALOG.read_bytes(), f"local_bright_catalog:{LOCAL_BRIGHT_CATALOG}"
    raise RuntimeError("No remote catalog available and no local bright-star catalog found.")


def main() -> int:
    args = parse_args()
    site = load_site_settings(Path(args.settings))
    if site is None and any(value is None for value in (args.name, args.lat, args.lon, args.alt, args.timezone)):
        raise SystemExit("Faltan settings locales o sitio completo por CLI.")
    lat = args.lat if args.lat is not None else site.lat
    lon = args.lon if args.lon is not None else site.lon
    alt = args.alt if args.alt is not None else site.alt_m
    timezone_name = args.timezone or site.timezone
    timezone = ZoneInfo(timezone_name)
    start = datetime.fromisoformat(args.from_dt).astimezone(timezone)
    end = datetime.fromisoformat(args.to_dt).astimezone(timezone)
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt * u.m)
    corridor = moon_corridor(start, end, location)
    raw, source_label = tap_or_local_bright_csv(gaia_query(corridor, args.max_g_mag))
    if source_label.startswith("local_bright_catalog:"):
        validate_local_catalog(Path(source_label.split(":", 1)[1]), start, end, lat, lon, alt)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    diag = {"resolved_source": source_label, "corridor": corridor, "candidate_rows": max(0, raw.decode("utf-8", errors="replace").count("\n") - 1)}
    out.with_suffix(".diagnostic.json").write_text(json.dumps(diag, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"candidate_rows": diag["candidate_rows"], "out": str(out), "resolved_source": source_label}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
