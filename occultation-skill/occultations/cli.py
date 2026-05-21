from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .config import RunConfig, SiteConfig


def _as_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "y"}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Filtro local de ocultaciones astronómicas")
    p.add_argument("--name", required=True)
    p.add_argument("--lat", required=True, type=float)
    p.add_argument("--lon", required=True, type=float)
    p.add_argument("--alt", required=True, type=float)
    p.add_argument("--timezone", required=True)
    p.add_argument("--from", dest="from_dt", required=True)
    p.add_argument("--to", dest="to_dt", required=True)
    p.add_argument("--horizon-days", type=int, default=30)
    p.add_argument("--max-mag", type=float, default=11)
    p.add_argument("--min-alt", type=float, default=20)
    p.add_argument("--min-duration", type=float, default=0)
    p.add_argument("--include-subsecond", default="true")
    p.add_argument("--input", dest="input_path")
    p.add_argument("--raw-dir", default="data/raw")
    p.add_argument("--download", action="store_true", default=False)
    p.add_argument("--source-url", action="append", default=[])
    p.add_argument("--out", required=True)
    return p


def parse_args(argv: list[str] | None = None) -> RunConfig:
    ns = build_parser().parse_args(argv)
    site = SiteConfig(ns.name, ns.lat, ns.lon, ns.alt, ns.timezone)
    return RunConfig(
        site=site,
        from_dt=datetime.fromisoformat(ns.from_dt),
        to_dt=datetime.fromisoformat(ns.to_dt),
        horizon_days=ns.horizon_days,
        max_mag=ns.max_mag,
        min_alt=ns.min_alt,
        min_duration=ns.min_duration,
        include_subsecond=_as_bool(ns.include_subsecond),
        input_path=Path(ns.input_path) if ns.input_path else None,
        raw_dir=Path(ns.raw_dir),
        download=ns.download,
        source_urls=ns.source_url,
        out=Path(ns.out),
    )
