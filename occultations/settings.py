from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Callable

from .config import DEFAULT_SITE, SiteConfig

LOCAL_SETTINGS_PATH = Path("settings.local.json")


def load_site_settings(path: Path = LOCAL_SETTINGS_PATH) -> SiteConfig | None:
    if not path.exists():
        return None

    payload = json.loads(path.read_text(encoding="utf-8"))
    site = payload.get("site", payload)
    return SiteConfig(
        name=str(site["name"]),
        lat=float(site["lat"]),
        lon=float(site["lon"]),
        alt_m=float(site.get("alt_m", site.get("alt"))),
        timezone=str(site["timezone"]),
    )


def save_site_settings(site: SiteConfig, path: Path = LOCAL_SETTINGS_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"site": asdict(site)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def prompt_site_settings(
    default: SiteConfig = DEFAULT_SITE,
    input_fn: Callable[[str], str] = input,
) -> SiteConfig:
    print("No hay settings locales. Configura primero el observatorio base.")
    return SiteConfig(
        name=_prompt_text("Nombre", default.name, input_fn),
        lat=_prompt_float("Latitud", default.lat, input_fn),
        lon=_prompt_float("Longitud", default.lon, input_fn),
        alt_m=_prompt_float("Altitud en metros", default.alt_m, input_fn),
        timezone=_prompt_text("Zona horaria", default.timezone, input_fn),
    )


def _prompt_text(label: str, default: str, input_fn: Callable[[str], str]) -> str:
    value = input_fn(f"{label} [{default}]: ").strip()
    return value or default


def _prompt_float(label: str, default: float, input_fn: Callable[[str], str]) -> float:
    value = input_fn(f"{label} [{default}]: ").strip()
    return float(value) if value else default
