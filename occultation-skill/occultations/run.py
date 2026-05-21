from __future__ import annotations

from datetime import datetime, timezone
from dataclasses import asdict
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from occultations.astronomy import compute_observables, to_local
from occultations.cli import parse_args
from occultations.download import download_sources
from occultations.filters import is_observable
from occultations.parser import parse_events
from occultations.report import PENDING_TEXT, write_reports
from occultations.scoring import score_event


def main() -> int:
    cfg = parse_args()
    sources: list[Path] = []
    if cfg.download and cfg.source_urls:
        sources.extend(download_sources(cfg.source_urls, cfg.raw_dir))
    if cfg.input_path:
        sources.append(cfg.input_path)
    if not sources:
        sources.extend(sorted(cfg.raw_dir.glob("*.csv")))
    if not sources:
        raise SystemExit("No hay fuentes para procesar. Usa --input o coloca ficheros en data/raw/.")

    events, discarded = [], []
    for src in sources:
        for e in parse_events(src):
            if not e.utc_datetime:
                continue
            d = asdict(e)
            d.update(compute_observables(e.utc_datetime, cfg.site.lat, cfg.site.lon, cfg.site.alt_m, e.ra, e.dec))
            d["local_datetime"] = to_local(e.utc_datetime, cfg.site.timezone).isoformat()
            d["utc_datetime"] = e.utc_datetime
            d["geometry"] = {"inside_shadow": None, "central_line_distance_km": None, "local_duration_s": None, "local_probability": None, "local_zone": None, "status": "pending_validation"}
            ok, reasons = is_observable(d, cfg)
            s1, s2, st, sr, risks, rec = score_event(d)
            d.update({"score_science": s1, "score_operational": s2, "score_total": st, "recommendation": rec, "reason": reasons + sr, "risks": risks})
            if ok:
                d["utc_datetime"] = d["utc_datetime"].isoformat()
                events.append(d)
            else:
                discarded.append({"event": d.get("object_name"), "reason": "; ".join(reasons)})

    best = max(events, key=lambda x: x["score_total"], default=None)
    payload = {
        "site": {"name": cfg.site.name, "lat": cfg.site.lat, "lon": cfg.site.lon, "alt_m": cfg.site.alt_m, "timezone": cfg.site.timezone},
        "window": {"from_local": cfg.from_dt.isoformat(), "to_local": cfg.to_dt.isoformat(), "from_utc": cfg.from_dt.astimezone(timezone.utc).isoformat(), "to_utc": cfg.to_dt.astimezone(timezone.utc).isoformat(), "horizon_days": cfg.horizon_days},
        "sources": [str(x) for x in sources],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"total_events": len(events)+len(discarded), "observable_events": len(events), "recommended_events": sum(1 for x in events if x["recommendation"]=="recommended"), "best_event": best.get("object_name") if best else None, "operational_priority": "high" if best and best["score_total"] >= 8 else "medium" if best and best["score_total"] >= 5 else "low"},
        "events": events,
        "discarded": discarded,
    }
    write_reports(payload, cfg.out)
    print(PENDING_TEXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
