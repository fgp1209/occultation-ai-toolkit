from occultations.scoring import score_event


def test_scoring_bright_subsecond():
    event = {"object_type": "mba", "star_mag": 7.5, "max_duration_s": 0.3, "altitude_deg": 40, "sun_altitude_deg": -20, "moon_sep_deg": 30, "geometry": {"status": "pending_validation"}}
    sci, op, total, reasons, _, rec = score_event(event)
    assert sci >= 1
    assert op >= 1
    assert any("subsegundo" in r for r in reasons)
    assert rec == "pending_geometry"
