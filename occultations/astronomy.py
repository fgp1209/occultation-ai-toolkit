from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body
from astropy.time import Time
import astropy.units as u


def to_local(dt_utc: datetime, timezone: str) -> datetime:
    return dt_utc.astimezone(ZoneInfo(timezone))


def compute_observables(dt_utc: datetime, lat: float, lon: float, alt_m: float, ra: str | None, dec: str | None) -> dict[str, float | None]:
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt_m * u.m)
    t = Time(dt_utc)
    altaz = AltAz(obstime=t, location=location)
    sun_alt = get_body("sun", t, location).transform_to(altaz).alt.deg
    moon = get_body("moon", t, location)

    altitude = azimuth = moon_sep = None
    if ra and dec:
        target = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
        target_altaz = target.transform_to(altaz)
        altitude = float(target_altaz.alt.deg)
        azimuth = float(target_altaz.az.deg)
        moon_sep = float(target.separation(moon).deg)

    return {
        "altitude_deg": altitude,
        "azimuth_deg": azimuth,
        "moon_sep_deg": moon_sep,
        "sun_altitude_deg": float(sun_alt),
    }
