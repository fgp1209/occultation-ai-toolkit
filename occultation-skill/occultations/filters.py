from __future__ import annotations

from .config import OccultationEvent, RunConfig


def is_observable(event: dict, cfg: RunConfig) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if event["utc_datetime"] < cfg.from_dt.astimezone(event["utc_datetime"].tzinfo) or event["utc_datetime"] > cfg.to_dt.astimezone(event["utc_datetime"].tzinfo):
        reasons.append("Fuera de ventana temporal")
    if event.get("star_mag") is not None and event["star_mag"] > cfg.max_mag:
        reasons.append("Estrella demasiado débil")
    if event.get("altitude_deg") is not None and event["altitude_deg"] < cfg.min_alt:
        reasons.append("Altura insuficiente")
    if event.get("sun_altitude_deg") is not None and event["sun_altitude_deg"] > -6:
        reasons.append("Sol no suficientemente bajo")
    if event.get("max_duration_s") is not None and event["max_duration_s"] < cfg.min_duration:
        reasons.append("Duración insuficiente")
    return len(reasons) == 0, reasons


def to_dict(evt: OccultationEvent) -> dict:
    from dataclasses import asdict
    return asdict(evt)
