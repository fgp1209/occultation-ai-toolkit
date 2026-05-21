from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from occultations.lunar import LunarCandidate, detect_lunar_occultations, score_lunar_event, write_lunar_reports
from tools.build_sabadell_final_report import build


def test_lunar_detector_does_not_invent_offset_synthetic_candidate():
    start = datetime(2026, 5, 24, 21, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    end = datetime(2026, 5, 25, 1, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    candidate = LunarCandidate("synthetic", 0.0, -80.0, 7.0)

    events = detect_lunar_occultations([candidate], start, end, 41.548, 2.107, 220, "Europe/Madrid", "fixture.csv")

    assert events == []


def test_lunar_score_prefers_bright_high_event():
    score, reasons, _ = score_lunar_event(
        {
            "star_mag": 5.5,
            "moon_altitude_deg": 50,
            "moon_illuminated_fraction": 0.25,
            "event_type": "disappearance",
            "limb": None,
        }
    )

    assert score >= 8
    assert "Bright star" in reasons


def test_lunar_report_and_final_section(tmp_path: Path):
    payload = {
        "site": {"name": "OBS", "timezone": "Europe/Madrid"},
        "window": {"from_local": "a", "to_local": "b"},
        "source": {"catalog": "Gaia DR3 TAP candidate CSV", "calculation": "fixture"},
        "summary": {"candidate_stars": 1, "visible_events": 0},
        "events": [],
        "limitations": ["fixture limitation"],
    }
    _, md_path = write_lunar_reports(payload, tmp_path / "lunar")
    assert "No se encontraron ocultaciones lunares visibles" in md_path.read_text(encoding="utf-8")

    week = {
        "site": {"timezone": "Europe/Madrid"},
        "window": {"from_local": "2026-05-24T21:00:00+02:00", "to_local": "2026-05-25T07:00:00+02:00"},
        "summary": {"total_events": 1, "observable_events": 0, "recommended_events": 0, "operational_priority": "low"},
        "events": [],
        "discarded": [],
    }
    final = build(week, week, payload)
    assert "## Ocultaciones asteroidales" in final
    assert "## Ocultaciones lunares" in final
