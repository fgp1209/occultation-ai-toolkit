import json
from pathlib import Path

from occultations.cli import parse_args


def test_parse_args_uses_local_site_settings(tmp_path: Path):
    settings = tmp_path / "settings.local.json"
    settings.write_text(
        json.dumps(
            {
                "site": {
                    "name": "Observatori de Sabadell",
                    "lat": 41.550111,
                    "lon": 2.091453,
                    "alt_m": 224,
                    "timezone": "Europe/Madrid",
                }
            }
        ),
        encoding="utf-8",
    )

    cfg = parse_args(
        [
            "--settings",
            str(settings),
            "--from",
            "2026-05-24T21:00:00+02:00",
            "--to",
            "2026-05-25T04:00:00+02:00",
            "--out",
            str(tmp_path / "report"),
        ]
    )

    assert cfg.site.name == "Observatori de Sabadell"
    assert cfg.site.timezone == "Europe/Madrid"
    assert cfg.site.alt_m == 224


def test_parse_args_persists_site_passed_on_first_run(tmp_path: Path):
    settings = tmp_path / "settings.local.json"

    cfg = parse_args(
        [
            "--settings",
            str(settings),
            "--name",
            "Observatori de Sabadell",
            "--lat",
            "41.550111",
            "--lon",
            "2.091453",
            "--alt",
            "224",
            "--timezone",
            "Europe/Madrid",
            "--from",
            "2026-05-24T21:00:00+02:00",
            "--to",
            "2026-05-25T04:00:00+02:00",
            "--out",
            str(tmp_path / "report"),
        ]
    )

    assert settings.exists()
    assert cfg.site.lat == 41.550111
    assert cfg.site.lon == 2.091453
