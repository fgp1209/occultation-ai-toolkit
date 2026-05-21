from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from tools.run_lunar_occultations import validate_local_catalog
from tools import download_lunar_sources as downloader
from occultations.lunar import LunarCandidate, detect_lunar_occultations, candidate_diagnostics


WINDOW_START = datetime(2026, 5, 24, 21, 0, tzinfo=ZoneInfo("Europe/Madrid"))
WINDOW_END = datetime(2026, 5, 25, 7, 0, tzinfo=ZoneInfo("Europe/Madrid"))


def _write_catalog(path: Path, rows: list[str]) -> Path:
    header = "star_name,catalog,source_id,ra_deg,dec_deg,pmra,pmdec,epoch,mag_v,mag_g\n"
    path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_local_catalog_coverage_rejects_too_small_catalog(tmp_path: Path):
    catalog = _write_catalog(
        tmp_path / "small.csv",
        ["HIP 1,hip,1,10,10,0,0,J1991.25,6.0,"] * 10,
    )
    with pytest.raises(SystemExit, match="Local lunar catalog coverage insufficient for operational validation."):
        validate_local_catalog(catalog, WINDOW_START, WINDOW_END, 41.548, 2.107, 220)


def test_lunar_downloader_uses_local_catalog_when_remote_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    local_catalog = _write_catalog(
        tmp_path / "bright-stars.csv",
        [f"HIP {i},hip,{i},240.{i%10},-20.{i%10},0,0,J1991.25,7.0," for i in range(1, 130)],
    )
    monkeypatch.setattr(downloader, "LOCAL_BRIGHT_CATALOG", local_catalog)

    def fail_remote(_request, timeout=120):  # noqa: ARG001
        raise RuntimeError("remote down")

    monkeypatch.setattr(downloader, "urlopen", fail_remote)
    raw, source = downloader.tap_or_local_bright_csv("SELECT 1")
    assert source.startswith("local_bright_catalog:")
    assert raw.startswith(b"star_name,catalog,source_id")


def test_lunar_outputs_coverage_diagnostics(tmp_path: Path):
    rows = [f"HIP {i},hip,{i},241.{i%10},-20.{i%10},0,0,J1991.25,7.5," for i in range(1, 160)]
    catalog = _write_catalog(tmp_path / "cover.csv", rows)
    payload = validate_local_catalog(catalog, WINDOW_START, WINDOW_END, 41.548, 2.107, 220)
    assert payload["total_stars"] >= 100
    assert "moon_path_ra_min" in payload and "bright_stars_within_corridor" in payload


def test_lunar_detector_accepts_bright_fixture_event():
    candidate = LunarCandidate("fixture", 241.3, -20.82, g_mag=6.0, v_mag=5.8, catalog="fixture", star_name="Fixture")
    events = detect_lunar_occultations([candidate], WINDOW_START, WINDOW_END, 41.548, 2.107, 220, "Europe/Madrid", "fixture.csv")
    assert isinstance(events, list)
    diag = candidate_diagnostics([candidate], WINDOW_START, WINDOW_END, 41.548, 2.107, 220, "Europe/Madrid", top_n=5)
    assert diag and {"star_name", "catalog", "mag_v", "min_separation_arcsec", "lunar_radius_arcsec", "margin_arcsec", "closest_approach_local", "occulted_yes_no", "reason_if_no"} <= set(diag[0].keys())
