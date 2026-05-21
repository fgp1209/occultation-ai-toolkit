from datetime import datetime, timezone
from occultations.config import RunConfig, SiteConfig
from occultations.filters import is_observable


def test_discard_low_altitude():
    cfg = RunConfig(site=SiteConfig("x", 0, 0, 0, "UTC"), from_dt=datetime(2026,5,1,tzinfo=timezone.utc), to_dt=datetime(2026,5,2,tzinfo=timezone.utc), min_alt=20)
    ok, reasons = is_observable({"utc_datetime": datetime(2026,5,1,12,tzinfo=timezone.utc), "altitude_deg": 10, "sun_altitude_deg": -10, "star_mag": 9, "max_duration_s": 1}, cfg)
    assert not ok
    assert "Altura insuficiente" in reasons
