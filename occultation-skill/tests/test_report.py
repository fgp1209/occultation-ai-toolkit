from pathlib import Path
from occultations.report import write_reports, PENDING_TEXT


def test_markdown_pending_geometry(tmp_path: Path):
    payload = {"site": {"name": "OBS", "timezone": "Europe/Madrid"}, "window": {"from_local": "a", "to_local": "b"}, "sources": ["x.csv"], "generated_at": "now", "summary": {"total_events":1}, "events": [{"local_datetime":"2026-01-01T20:00:00+01:00","object_name":"Q","object_type":"tno","star_name":"S","star_mag":9,"max_duration_s":0.4,"altitude_deg":30,"score_science":9,"score_operational":5,"score_total":7,"recommendation":"pending_geometry","geometry":{"status":"pending_validation"}}]}
    _, md = write_reports(payload, tmp_path / "r")
    assert PENDING_TEXT in md.read_text(encoding="utf-8")
