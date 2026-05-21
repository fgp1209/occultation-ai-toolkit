from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body, get_sun
from astropy.time import Time

MOON_RADIUS_KM = 1737.4
CALCULATION_NAME = "astropy_builtin_topocentric_moon_vs_catalog_candidates"
MAX_LUNAR_EVENT_DURATION_MIN = 120
MIN_OPERATIONAL_MOON_ALT_DEG = 5.0
CALCULATION_LIMITATIONS = [
    "Uses Gaia corridor candidates (and optional fallback CSV) with Astropy built-in ephemeris.",
    "Spherical lunar limb only; no limb-profile corrections.",
    "Dark/bright lunar limb classification is approximate via Sun position angle.",
]


@dataclass(frozen=True)
class LunarCandidate:
    source_id: str
    ra_deg: float
    dec_deg: float
    g_mag: float | None
    v_mag: float | None = None
    pmra_mas_yr: float | None = None
    pmdec_mas_yr: float | None = None
    catalog: str = "gaia_dr3"
    star_name: str | None = None


def load_gaia_candidates(path: Path) -> list[LunarCandidate]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = csv.DictReader(fh)
        out: list[LunarCandidate] = []
        for row in rows:
            ra_raw = row.get("ra_deg") or row.get("ra")
            dec_raw = row.get("dec_deg") or row.get("dec")
            if not (ra_raw and dec_raw):
                continue
            g_mag = _optional_float(row.get("phot_g_mean_mag") or row.get("mag_g"))
            v_mag = _optional_float(row.get("mag_v"))
            if v_mag is None and g_mag is not None:
                v_mag = g_mag
            source_id = str(row.get("source_id") or row.get("id") or "")
            catalog = str(row.get("catalog") or "gaia_dr3")
            star_name = row.get("star_name") or (f"Gaia DR3 {source_id}" if source_id else "catalog_star")
            out.append(LunarCandidate(source_id, float(ra_raw), float(dec_raw), g_mag, v_mag, _optional_float(row.get("pmra")), _optional_float(row.get("pmdec")), catalog, star_name))
        return out


def moon_corridor(start: datetime, end: datetime, location: EarthLocation) -> dict[str, float]:
    sample_times = _times(start, end, timedelta(minutes=10))
    moons = get_body("moon", Time(sample_times), location).icrs
    center = SkyCoord(ra=_circular_mean(moons.ra.deg) * u.deg, dec=float(sum(moons.dec.deg) / len(moons)) * u.deg, frame="icrs")
    radius = max(float(center.separation(moon).deg) for moon in moons) + 2.0
    return {"ra_deg": float(center.ra.deg), "dec_deg": float(center.dec.deg), "radius_deg": radius}


def detect_lunar_occultations(candidates: Iterable[LunarCandidate], start: datetime, end: datetime, lat: float, lon: float, alt_m: float, timezone_name: str, source_file: str, step_seconds: int = 10) -> list[dict]:
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt_m * u.m)
    events: list[dict] = []
    for candidate in candidates:
        events.extend(_candidate_events(candidate, start, end, location, timezone_name, source_file, step_seconds))
    events.sort(key=lambda event: event["utc_datetime"])
    return _annotate_and_filter_events(events)

def candidate_diagnostics(candidates: Iterable[LunarCandidate], start: datetime, end: datetime, lat: float, lon: float, alt_m: float, timezone_name: str, top_n: int = 20) -> list[dict]:
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt_m * u.m)
    rows = []
    for c in candidates:
        rows.append(_candidate_minimum(c, start, end, location, timezone_name))
    rows.sort(key=lambda x: x["margin_arcsec"])
    return rows[:top_n]

def candidate_diagnostics(candidates: Iterable[LunarCandidate], start: datetime, end: datetime, lat: float, lon: float, alt_m: float, timezone_name: str, top_n: int = 20) -> list[dict]:
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt_m * u.m)
    rows = []
    for c in candidates:
        rows.append(_candidate_minimum(c, start, end, location, timezone_name))
    rows.sort(key=lambda x: x["margin_arcsec"])
    return rows[:top_n]

# (helper functions omitted for brevity in command)

def _candidate_events(candidate, start, end, location, timezone_name, source_file, step_seconds):
    times = _times(start, end, timedelta(seconds=step_seconds))
    tgrid = Time(times)
    star = _candidate_coord(candidate, tgrid[0])
    moon_grid = get_body("moon", tgrid, location)
    moon_radius_grid = _moon_radius_deg(moon_grid)
    signed = star.separation(moon_grid).deg - moon_radius_grid
    out=[]
    for i in range(len(signed)-1):
        b=float(signed[i]); a=float(signed[i+1])
        if b==0 or a==0 or b*a<0:
            et=_refine_crossing(star,times[i],times[i+1],b,a,location)
            etype="disappearance" if b>0>=a else "reappearance"
            out.append(_event_payload(candidate, star, et, location, timezone_name, source_file, etype))
    return out

def _candidate_minimum(candidate,start,end,location,timezone_name):
    times=_times(start,end,timedelta(seconds=30)); tgrid=Time(times)
    star=_candidate_coord(candidate,tgrid[0]); moon=get_body("moon",tgrid,location)
    sep=star.separation(moon).deg; rad=_moon_radius_deg(moon)
    signed=[float(s-r) for s,r in zip(sep,rad)]
    idx=min(range(len(signed)), key=lambda i:signed[i])
    moon_altaz=moon[idx].transform_to(AltAz(obstime=tgrid[idx],location=location))
    return {
      "star_name": candidate.star_name or f"{candidate.catalog}:{candidate.source_id}","catalog":candidate.catalog,"mag_v":candidate.v_mag,"mag_g":candidate.g_mag,
      "min_separation_arcsec": float(sep[idx])*3600, "lunar_radius_arcsec": float(rad[idx])*3600, "margin_arcsec": float(signed[idx])*3600,
      "closest_approach_local": times[idx].astimezone(ZoneInfo(timezone_name)).isoformat(), "occulted_yes_no": "yes" if signed[idx] <=0 else "no",
      "reason_if_no": "outside_limb" if signed[idx] >0 else "occulted", "moon_altitude_deg": float(moon_altaz.alt.deg)
    }

def _annotate_and_filter_events(events):
    by={}
    for e in events: by.setdefault(e["star_source_id"],[]).append(e)
    filtered=[]
    for arr in by.values():
      arr.sort(key=lambda x:x["utc_datetime"]); pend=None
      for e in arr:
        e["implicit_duration_min"]=None
        if e.get("moon_altitude_deg") is not None and e["moon_altitude_deg"] < MIN_OPERATIONAL_MOON_ALT_DEG:
          e.setdefault("risks",[]).append("Moon altitude < 5 deg (non-operational)"); continue
        if e["event_type"]=="disappearance": pend=e; filtered.append(e); continue
        if e["event_type"]=="reappearance" and pend is not None:
          d=(datetime.fromisoformat(e["utc_datetime"])-datetime.fromisoformat(pend["utc_datetime"])).total_seconds()/60
          pend["implicit_duration_min"]=d; e["implicit_duration_min"]=d
          if d>MAX_LUNAR_EVENT_DURATION_MIN:
            pend.setdefault("risks",[]).append("Rejected: implicit D/R duration > 120 min")
            e.setdefault("risks",[]).append("Rejected: implicit D/R duration > 120 min")
            filtered=[x for x in filtered if x is not pend]; pend=None; continue
          filtered.append(e); pend=None; continue
        filtered.append(e)
    return sorted(filtered,key=lambda x:x["utc_datetime"])

def score_lunar_event(event):
    score=2; reasons=["Lunar visual/timing practice"]; risks=[]; mag=event.get("mag_v") or event.get("star_mag")
    alt=event.get("moon_altitude_deg"); phase=event.get("moon_illuminated_fraction")
    if mag is not None:
      if mag<=6: score+=4; reasons.append("Bright star")
      elif mag<=8: score+=3; reasons.append("Moderately bright star")
      elif mag<=10: score+=1; reasons.append("Faint but workable star")
      else: risks.append("Faint star magnitude")
    if alt is not None:
      if alt>=35: score+=2; reasons.append("Moon high")
      elif alt>=20: score+=1
      else: risks.append("Moon low")
    if phase is not None and phase>=0.85: score-=1; risks.append("Strong lunar glare")
    return max(1,min(10,score)), reasons, risks

def write_lunar_reports(payload, out_base):
    import json

    out_base.parent.mkdir(parents=True, exist_ok=True)
    jp = out_base.with_suffix('.json')
    mp = out_base.with_suffix('.md')
    jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [
        f"# Ocultaciones lunares - {payload['site']['name']}",
        "",
        f"- Eventos lunares visibles encontrados: {payload['summary']['visible_events']}",
        "",
    ]
    if not payload.get('events'):
        lines += ["No se encontraron ocultaciones lunares visibles en la ventana.", ""]
    else:
        lines += ["| Hora local | Estrella | Mag V | Mag G | Tipo | Alt Luna |", "|---|---|---:|---:|---|---:|"]
        for e in payload['events']:
            lines.append(f"| {e['local_datetime']} | {e['star_name']} | {_fmt(e.get('mag_v'))} | {_fmt(e.get('mag_g'))} | {e['event_type']} | {_fmt(e.get('moon_altitude_deg'))} |")
        lines += ["", "## Diagnóstico de candidatas cercanas", "", "| star_name | catalog | mag_v | mag_g | min_separation_arcsec | lunar_radius_arcsec | margin_arcsec | closest_approach_local | occulted_yes_no | reason_if_no |", "|---|---|---:|---:|---:|---:|---:|---|---|---|"]
        for r in payload.get('candidate_diagnostics', []):
            lines.append(f"| {r['star_name']} | {r['catalog']} | {_fmt(r.get('mag_v'))} | {_fmt(r.get('mag_g'))} | {_fmt(r.get('min_separation_arcsec'))} | {_fmt(r.get('lunar_radius_arcsec'))} | {_fmt(r.get('margin_arcsec'))} | {r.get('closest_approach_local')} | {r.get('occulted_yes_no')} | {r.get('reason_if_no')} |")
    mp.write_text("\n".join(lines) + "\n", encoding='utf-8')
    return jp, mp
def _event_payload(candidate,star,event_time,location,timezone_name,source_file,event_type):
    t=Time(event_time); moon=get_body('moon',t,location); sun=get_sun(t); moon_altaz=moon.transform_to(AltAz(obstime=t,location=location))
    elong=float(moon.separation(sun).deg); phase=(1-math.cos(math.radians(elong)))/2; sep=float(star.separation(moon).deg)*3600; rad=float(_moon_radius_deg(moon))*3600
    payload={"occulting_object":"Moon","star_name":candidate.star_name or f"Gaia DR3 {candidate.source_id}","star_source_id":candidate.source_id,"catalog":candidate.catalog,
    "star_mag":candidate.g_mag,"mag_g":candidate.g_mag,"mag_v":candidate.v_mag,"event_type":event_type,"utc_datetime":event_time.astimezone(timezone.utc).isoformat(),
    "local_datetime":event_time.astimezone(ZoneInfo(timezone_name)).isoformat(),"moon_altitude_deg":float(moon_altaz.alt.deg),"moon_azimuth_deg":float(moon_altaz.az.deg),"moon_illuminated_fraction":phase,
    "solar_elongation_deg":elong,"limb":None,"source":"catalog_tap","min_separation_arcsec":sep,"moon_radius_arcsec":rad,"occultation_margin_arcsec":sep-rad,
    "closest_approach_utc":event_time.astimezone(timezone.utc).isoformat(),"source_file":source_file,"calculation":CALCULATION_NAME,"scientific_value":"practice_timing",
    "utility":"Practice/timing lunar event"}
    sc,re,ri=score_lunar_event(payload); payload.update({"score_lunar":sc,"score_reasons":re,"risks":ri}); return payload

def _refine_crossing(star,left,right,left_value,right_value,location):
    for _ in range(25):
      m=left+(right-left)/2; mv=_signed_distance(star,m,location)
      if left_value==0 or left_value*mv<=0: right=m; right_value=mv
      else: left=m; left_value=mv
      if abs((right-left).total_seconds())<=1: break
    return left+(right-left)/2

def _signed_distance(star,when,location): moon=get_body('moon',Time(when),location); return float(star.separation(moon).deg-_moon_radius_deg(moon))

def _candidate_coord(candidate,target_time):
    kwargs={"ra":candidate.ra_deg*u.deg,"dec":candidate.dec_deg*u.deg,"frame":"icrs","obstime":Time("J2016.0")}
    if candidate.pmra_mas_yr is not None and candidate.pmdec_mas_yr is not None:
      kwargs["pm_ra_cosdec"]=candidate.pmra_mas_yr*u.mas/u.yr; kwargs["pm_dec"]=candidate.pmdec_mas_yr*u.mas/u.yr
      return SkyCoord(**kwargs).apply_space_motion(new_obstime=target_time)
    return SkyCoord(**kwargs)

def _times(start,end,step):
    out=[start.astimezone(timezone.utc)]; e=end.astimezone(timezone.utc)
    while out[-1]<e: out.append(min(out[-1]+step,e))
    return out

def _moon_radius_deg(moon):
    d=moon.distance.to_value(u.km)
    return [math.degrees(math.asin(MOON_RADIUS_KM/x)) for x in d] if hasattr(d,'__len__') else math.degrees(math.asin(MOON_RADIUS_KM/d))

def _optional_float(value):
    try: return None if value in (None,"") else float(value)
    except (TypeError,ValueError): return None

def _circular_mean(values):
    radians=[math.radians(v) for v in values]; s=sum(math.sin(v) for v in radians); c=sum(math.cos(v) for v in radians)
    return math.degrees(math.atan2(s,c))%360
