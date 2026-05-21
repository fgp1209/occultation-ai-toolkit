from __future__ import annotations

import csv
import math
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body, get_sun
from astropy.time import Time

MOON_RADIUS_KM = 1737.4
CALCULATION_NAME = "astropy_builtin_topocentric_moon_vs_gaia_dr3"
MAX_LUNAR_EVENT_DURATION_MIN = 120
MIN_OPERATIONAL_MOON_ALT_DEG = 5.0
CALCULATION_LIMITATIONS = [
    "Uses Gaia DR3 corridor candidates and Astropy's built-in solar-system ephemeris.",
    "Uses a spherical lunar limb; mountains, valleys, Besselian limb corrections, double stars and timing-grade reductions are not modeled.",
    "Gaia proper motions are applied only when both pmra and pmdec are present.",
    "Dark or bright lunar limb is not classified yet; it is reported as n/i.",
]


@dataclass(frozen=True)
class LunarCandidate:
    source_id: str
    ra_deg: float
    dec_deg: float
    g_mag: float | None
    pmra_mas_yr: float | None = None
    pmdec_mas_yr: float | None = None


def load_gaia_candidates(path: Path) -> list[LunarCandidate]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = csv.DictReader(fh)
        return [
            LunarCandidate(
                source_id=str(row.get("source_id") or ""),
                ra_deg=float(row["ra"]),
                dec_deg=float(row["dec"]),
                g_mag=_optional_float(row.get("phot_g_mean_mag")),
                pmra_mas_yr=_optional_float(row.get("pmra")),
                pmdec_mas_yr=_optional_float(row.get("pmdec")),
            )
            for row in rows
            if row.get("ra") and row.get("dec")
        ]


def moon_corridor(start: datetime, end: datetime, location: EarthLocation) -> dict[str, float]:
    sample_times = _times(start, end, timedelta(minutes=30))
    moons = get_body("moon", Time(sample_times), location).icrs
    center = SkyCoord(
        ra=_circular_mean(moons.ra.deg) * u.deg,
        dec=float(sum(moons.dec.deg) / len(moons)) * u.deg,
        frame="icrs",
    )
    radius = max(float(center.separation(moon).deg) for moon in moons) + 1.5
    return {"ra_deg": float(center.ra.deg), "dec_deg": float(center.dec.deg), "radius_deg": radius}


def detect_lunar_occultations(
    candidates: Iterable[LunarCandidate],
    start: datetime,
    end: datetime,
    lat: float,
    lon: float,
    alt_m: float,
    timezone_name: str,
    source_file: str,
    step_seconds: int = 30,
) -> list[dict]:
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt_m * u.m)
    times = _times(start, end, timedelta(seconds=step_seconds))
    time_grid = Time(times)
    moon_grid = get_body("moon", time_grid, location)
    moon_radius_grid = _moon_radius_deg(moon_grid)
    events: list[dict] = []
    for candidate in candidates:
        star = _candidate_coord(candidate, time_grid[0])
        signed = star.separation(moon_grid).deg - moon_radius_grid
        for index in range(len(signed) - 1):
            before = float(signed[index])
            after = float(signed[index + 1])
            if before == 0 or after == 0 or before * after < 0:
                event_time = _refine_crossing(
                    star,
                    times[index],
                    times[index + 1],
                    before,
                    after,
                    location,
                )
                event = _event_payload(
                    candidate,
                    star,
                    event_time,
                    location,
                    timezone_name,
                    source_file,
                    "disappearance" if before > 0 >= after else "reappearance",
                )
                if event["moon_altitude_deg"] is not None and event["moon_altitude_deg"] > 0:
                    events.append(event)
    events.sort(key=lambda event: event["utc_datetime"])
    events = _annotate_and_filter_events(events)
    return events




def _annotate_and_filter_events(events: list[dict]) -> list[dict]:
    by_star: dict[str, list[dict]] = {}
    for event in events:
        by_star.setdefault(event["star_source_id"], []).append(event)

    filtered: list[dict] = []
    for star_events in by_star.values():
        star_events.sort(key=lambda item: item["utc_datetime"])
        pending_disappearance: dict | None = None
        for event in star_events:
            event["implicit_duration_min"] = None
            if event.get("moon_altitude_deg") is not None and event["moon_altitude_deg"] < MIN_OPERATIONAL_MOON_ALT_DEG:
                event.setdefault("risks", []).append("Moon altitude < 5 deg (non-operational)")
                continue
            if event["event_type"] == "disappearance":
                pending_disappearance = event
                filtered.append(event)
                continue
            if event["event_type"] == "reappearance" and pending_disappearance is not None:
                dt0 = datetime.fromisoformat(pending_disappearance["utc_datetime"])
                dt1 = datetime.fromisoformat(event["utc_datetime"])
                duration_min = (dt1 - dt0).total_seconds() / 60.0
                pending_disappearance["implicit_duration_min"] = duration_min
                event["implicit_duration_min"] = duration_min
                if duration_min > MAX_LUNAR_EVENT_DURATION_MIN:
                    pending_disappearance.setdefault("risks", []).append("Rejected: implicit D/R duration > 120 min")
                    event.setdefault("risks", []).append("Rejected: implicit D/R duration > 120 min")
                    filtered = [e for e in filtered if e is not pending_disappearance]
                    pending_disappearance = None
                    continue
                filtered.append(event)
                pending_disappearance = None
                continue
            filtered.append(event)
    filtered.sort(key=lambda item: item["utc_datetime"])
    return filtered

def score_lunar_event(event: dict) -> tuple[int, list[str], list[str]]:
    score = 2
    reasons: list[str] = ["Lunar visual/timing practice"]
    risks: list[str] = []
    mag = event.get("star_mag")
    altitude = event.get("moon_altitude_deg")
    phase = event.get("moon_illuminated_fraction")
    if mag is not None:
        if mag <= 6:
            score += 4
            reasons.append("Bright star")
        elif mag <= 8:
            score += 3
            reasons.append("Moderately bright star")
        elif mag <= 10:
            score += 1
            reasons.append("Faint but workable star")
        else:
            risks.append("Faint Gaia G magnitude")
    if altitude is not None:
        if altitude >= 35:
            score += 2
            reasons.append("Moon high")
        elif altitude >= 20:
            score += 1
            reasons.append("Moon altitude moderate")
        else:
            risks.append("Moon low")
            if altitude < MIN_OPERATIONAL_MOON_ALT_DEG:
                risks.append("Non-operational altitude (<5 deg)")
    if phase is not None:
        if phase >= 0.85:
            score -= 1
            risks.append("Strong lunar glare")
        elif phase <= 0.35:
            score += 1
            reasons.append("Lower illuminated fraction")
    if event.get("event_type") == "disappearance":
        reasons.append("Disappearance")
    if event.get("limb") in {"dark", "bright"}:
        reasons.append(f"{event['limb'].title()} limb")
    return max(1, min(10, score)), reasons, risks


def write_lunar_reports(payload: dict, out_base: Path) -> tuple[Path, Path]:
    import json

    out_base.parent.mkdir(parents=True, exist_ok=True)
    json_path = out_base.with_suffix(".json")
    md_path = out_base.with_suffix(".md")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        f"# Ocultaciones lunares - {payload['site']['name']}",
        "",
        "## Ventana",
        f"- Inicio local: {payload['window']['from_local']}",
        f"- Fin local: {payload['window']['to_local']}",
        f"- Fuente estelar: {payload['source']['catalog']}",
        f"- Calculo: {payload['source']['calculation']}",
        f"- Candidatas Gaia evaluadas: {payload['summary']['candidate_stars']}",
        f"- Eventos lunares visibles encontrados: {payload['summary']['visible_events']}",
        "",
    ]
    if not payload["events"]:
        lines += ["## Resultado", "", "No se encontraron ocultaciones lunares visibles en la ventana.", ""]
    else:
        lines += [
            "## Eventos",
            "",
            "| Hora local | Hora UTC | Objeto ocultador | Estrella | Mag G | Tipo | Altura lunar | Fase | Elongacion solar | Score |",
            "|---|---|---|---|---:|---|---:|---:|---:|---:|",
        ]
        for event in payload["events"]:
            lines.append(
                f"| {event['local_datetime']} | {event['utc_datetime']} | Luna | {event['star_name']} | {_fmt(event.get('star_mag'))} | {event['event_type']} | {_fmt(event.get('moon_altitude_deg'))} | {_fmt(event.get('moon_illuminated_fraction'))} | {_fmt(event.get('solar_elongation_deg'))} | {event['score_lunar']}/10 |"
            )
        lines += ["", "## Detalle", ""]
        for index, event in enumerate(payload["events"], start=1):
            lines += [
                f"### {index}. {event['star_name']} - {event['event_type']}",
                "",
                "- Objeto ocultador: Luna",
                f"- Estrella: {event['star_name']}",
                f"- Magnitud Gaia G: {_fmt(event.get('star_mag'))}",
                f"- Hora local: {event['local_datetime']}",
                f"- Hora UTC: {event['utc_datetime']}",
                f"- Altura lunar: {_fmt(event.get('moon_altitude_deg'))}",
                f"- Fase lunar iluminada: {_fmt(event.get('moon_illuminated_fraction'))}",
                f"- Elongacion solar: {_fmt(event.get('solar_elongation_deg'))}",
                f"- Separacion minima: {_fmt(event.get('min_separation_arcsec'))} arcsec",
                f"- Radio lunar angular: {_fmt(event.get('moon_radius_arcsec'))} arcsec",
                f"- Margen (sep-radio): {_fmt(event.get('occultation_margin_arcsec'))} arcsec",
                f"- Instante minimo acercamiento UTC: {event.get('closest_approach_utc') or 'n/i'}",
                f"- Duracion implicita D/R: {_fmt(event.get('implicit_duration_min'))} min",
                f"- Limbo: {event.get('limb') or 'n/i'}",
                "- Valor cientifico: practica/timing lunar salvo caso especial no clasificado",
                f"- Utilidad practica: {event.get('utility')}",
                f"- Fuente/calculo: {payload['source']['calculation']} con {payload['source']['catalog']}",
                f"- Limitaciones: {'; '.join(payload['limitations'])}",
                "",
            ]
    lines += ["## Limitaciones", ""]
    lines.extend(f"- {item}" for item in payload["limitations"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def _event_payload(
    candidate: LunarCandidate,
    star: SkyCoord,
    event_time: datetime,
    location: EarthLocation,
    timezone_name: str,
    source_file: str,
    event_type: str,
) -> dict:
    t = Time(event_time)
    moon = get_body("moon", t, location)
    sun = get_sun(t)
    moon_altaz = moon.transform_to(AltAz(obstime=t, location=location))
    elongation = float(moon.separation(sun).deg)
    phase = (1 - math.cos(math.radians(elongation))) / 2
    min_sep_arcsec = abs(float(star.separation(moon).deg)) * 3600
    moon_radius_arcsec = float(_moon_radius_deg(moon)) * 3600
    margin_arcsec = min_sep_arcsec - moon_radius_arcsec
    payload = {
        "occulting_object": "Moon",
        "star_name": f"Gaia DR3 {candidate.source_id}",
        "star_source_id": candidate.source_id,
        "star_mag": candidate.g_mag,
        "event_type": event_type,
        "utc_datetime": event_time.astimezone(timezone.utc).isoformat(),
        "local_datetime": event_time.astimezone(ZoneInfo(timezone_name)).isoformat(),
        "moon_altitude_deg": float(moon_altaz.alt.deg),
        "moon_azimuth_deg": float(moon_altaz.az.deg),
        "moon_illuminated_fraction": phase,
        "solar_elongation_deg": elongation,
        "limb": None,
        "source": "gaia_dr3_tap",
        "min_separation_arcsec": min_sep_arcsec,
        "moon_radius_arcsec": moon_radius_arcsec,
        "occultation_margin_arcsec": margin_arcsec,
        "closest_approach_utc": event_time.astimezone(timezone.utc).isoformat(),
        "source_file": source_file,
        "calculation": CALCULATION_NAME,
        "scientific_value": "practice_timing",
        "utility": "Practice/timing lunar event; verify with timing-grade lunar prediction tools before precision work.",
    }
    score, reasons, risks = score_lunar_event(payload)
    payload.update({"score_lunar": score, "score_reasons": reasons, "risks": risks})
    return payload


def _refine_crossing(
    star: SkyCoord,
    left: datetime,
    right: datetime,
    left_value: float,
    right_value: float,
    location: EarthLocation,
) -> datetime:
    for _ in range(20):
        midpoint = left + (right - left) / 2
        mid_value = _signed_distance(star, midpoint, location)
        if left_value == 0 or left_value * mid_value <= 0:
            right = midpoint
            right_value = mid_value
        else:
            left = midpoint
            left_value = mid_value
        if abs((right - left).total_seconds()) <= 0.25:
            break
    return left + (right - left) / 2


def _signed_distance(star: SkyCoord, when: datetime, location: EarthLocation) -> float:
    moon = get_body("moon", Time(when), location)
    return float(star.separation(moon).deg - _moon_radius_deg(moon))


def _candidate_coord(candidate: LunarCandidate, target_time: Time) -> SkyCoord:
    kwargs = {
        "ra": candidate.ra_deg * u.deg,
        "dec": candidate.dec_deg * u.deg,
        "frame": "icrs",
        "obstime": Time("J2016.0"),
    }
    if candidate.pmra_mas_yr is not None and candidate.pmdec_mas_yr is not None:
        kwargs["pm_ra_cosdec"] = candidate.pmra_mas_yr * u.mas / u.yr
        kwargs["pm_dec"] = candidate.pmdec_mas_yr * u.mas / u.yr
        return SkyCoord(**kwargs).apply_space_motion(new_obstime=target_time)
    return SkyCoord(**kwargs)


def _times(start: datetime, end: datetime, step: timedelta) -> list[datetime]:
    times = [start.astimezone(timezone.utc)]
    while times[-1] < end.astimezone(timezone.utc):
        times.append(min(times[-1] + step, end.astimezone(timezone.utc)))
    return times


def _moon_radius_deg(moon) -> float | list[float]:
    distance = moon.distance.to_value(u.km)
    values = [math.degrees(math.asin(MOON_RADIUS_KM / item)) for item in distance] if hasattr(distance, "__len__") else math.degrees(math.asin(MOON_RADIUS_KM / distance))
    return values


def _optional_float(value: str | None) -> float | None:
    try:
        return float(value) if value not in {None, ""} else None
    except ValueError:
        return None


def _circular_mean(values) -> float:
    radians = [math.radians(float(value)) for value in values]
    return math.degrees(math.atan2(sum(math.sin(value) for value in radians), sum(math.cos(value) for value in radians))) % 360


def _fmt(value) -> str:
    if value is None or value == "":
        return "n/i"
    return f"{value:.3f}" if isinstance(value, float) else str(value)
