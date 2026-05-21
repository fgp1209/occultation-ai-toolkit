from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from occultations.parser import parse_events
from occultations.run import main as run_main
from occultations.scoring import score_event
from tools.normalize_raw_sources import normalize_raw_sources


def xml_event(day: int, hour_decimal: str, raw_id: str, name: str = "Sample") -> str:
    return f"""
  <Event>
    <Elements>JPL#fixture,0.1,2026,5,{day},{hour_decimal},0,0,0</Elements>
    <Earth>0,0,0,0,False</Earth>
    <Star>Gaia DR3 fixture,16.0,41.0,10.4,9.7,9.2,0.0,0,,16.1,41.1,0,0,0</Star>
    <Object>12345,{name},15.2,12.500,0,0,0,0,0,,0.8,0,0,0,</Object>
    <Errors>1.0,0.1</Errors>
    <ID>{raw_id},60000</ID>
  </Event>
"""


def write_xml(path: Path, *events: str) -> None:
    path.write_text("<Occultations>" + "".join(events) + "</Occultations>", encoding="utf-8")


def test_parse_iota_xml_basic(tmp_path: Path):
    raw = tmp_path / "fixture.xml"
    write_xml(raw, xml_event(23, "22.5", "fixture-1"))

    events = parse_events(raw)

    assert len(events) == 1
    assert events[0].utc_datetime.isoformat() == "2026-05-23T22:30:00+00:00"
    assert events[0].object_name == "(12345) Sample"
    assert events[0].star_name == "Gaia DR3 fixture"
    assert events[0].star_mag == 9.7
    assert events[0].ra == "16.1"
    assert events[0].dec == "41.1"
    assert events[0].source == "preston"


def test_normalize_raw_sources(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    write_xml(raw_dir / "fixture.xml", xml_event(23, "22.5", "fixture-1"))
    (raw_dir / "fixture.csv").write_text(
        "\ufeffobject_name,object_type,utc_datetime,star_name,star_mag,max_duration_s,mag_drop,ra,dec,source,source_url,raw_id\n"
        "(777) Csv,mba,2026-05-24T00:00:00+00:00,Csv star,8.2,,,,12.0,10.0,csv,,csv-1\n",
        encoding="utf-8",
    )
    out = tmp_path / "cache" / "normalized.csv"
    diagnostic = normalize_raw_sources(
        raw_dir,
        datetime.fromisoformat("2026-05-18T00:00:00+02:00"),
        datetime.fromisoformat("2026-06-17T23:59:59+02:00"),
        "Europe/Madrid",
        out,
    )

    assert out.read_bytes().startswith(b"object_name")
    with out.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 2
    assert diagnostic["events_passed_to_scorer"] == 2
    assert out.with_suffix(".diagnostic.json").exists()


def test_window_filter_local_timezone(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    write_xml(
        raw_dir / "boundary.xml",
        xml_event(17, "21.9997", "outside", "Outside"),
        xml_event(17, "22.0", "inside", "Inside"),
    )
    out = tmp_path / "normalized.csv"
    normalize_raw_sources(
        raw_dir,
        datetime(2026, 5, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),
        datetime(2026, 5, 24, 23, 59, 59, tzinfo=ZoneInfo("Europe/Madrid")),
        "Europe/Madrid",
        out,
    )

    with out.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert [row["raw_id"] for row in rows] == ["inside"]


def test_no_recommended_without_geometry():
    _, _, _, _, _, recommendation = score_event(
        {
            "object_type": "tno",
            "star_mag": 7.0,
            "max_duration_s": 3.0,
            "altitude_deg": 60,
            "sun_altitude_deg": -20,
            "moon_sep_deg": 90,
            "geometry": {"status": "pending_validation"},
        }
    )

    assert recommendation == "pending_geometry"


def test_end_to_end_sabadell(tmp_path: Path, monkeypatch):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    write_xml(raw_dir / "fixture.xml", xml_event(23, "22.5", "fixture-1"))
    normalized = tmp_path / "normalized.csv"
    normalize_raw_sources(
        raw_dir,
        datetime.fromisoformat("2026-05-18T00:00:00+02:00"),
        datetime.fromisoformat("2026-05-24T23:59:59+02:00"),
        "Europe/Madrid",
        normalized,
    )
    out = tmp_path / "report"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run.py",
            "--settings",
            str(tmp_path / "settings.json"),
            "--name",
            "Observatori de Sabadell",
            "--lat",
            "41.548",
            "--lon",
            "2.107",
            "--alt",
            "220",
            "--timezone",
            "Europe/Madrid",
            "--from",
            "2026-05-18T00:00:00+02:00",
            "--to",
            "2026-05-24T23:59:59+02:00",
            "--min-alt",
            "-90",
            "--input",
            str(normalized),
            "--out",
            str(out),
        ],
    )

    assert run_main() == 0
    payload = json.loads(out.with_suffix(".json").read_text(encoding="utf-8"))
    assert payload["sources"] == [str(normalized)]
    assert out.with_suffix(".md").exists()
