from datetime import datetime, timezone
from occultations.astronomy import to_local


def test_utc_to_madrid():
    dt = datetime(2026, 5, 24, 20, 0, tzinfo=timezone.utc)
    local = to_local(dt, "Europe/Madrid")
    assert local.hour == 22
