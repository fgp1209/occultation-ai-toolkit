from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

from .config import OccultationEvent

PARSER_VERSION = "iota-xml-v1"


def _parts(text: str | None) -> list[str]:
    if not text:
        return []
    return next(csv.reader([text], skipinitialspace=True))


def _float(raw: str | None) -> float | None:
    try:
        return float(raw) if raw not in {None, ""} else None
    except ValueError:
        return None


def _datetime_from_elements(parts: list[str]) -> datetime | None:
    if len(parts) < 6:
        return None
    try:
        midnight = datetime(int(parts[2]), int(parts[3]), int(parts[4]), tzinfo=timezone.utc)
        return midnight + timedelta(hours=float(parts[5]))
    except (TypeError, ValueError):
        return None


def _source_for(path: Path) -> str:
    parts = [part.lower() for part in path.parts]
    name = path.name.lower()
    is_iota = "iota" in parts or "iota-all" in name or name.endswith("-iota.zip")
    return "xml_iota" if is_iota else "preston"


def _object_type(parts: list[str]) -> str:
    context = " ".join(parts).lower()
    if "cubewano" in context:
        return "cubewano"
    if "centaur" in context:
        return "centaur"
    if "dwarf" in context:
        return "dwarf_planet"
    if "tno" in context or "trans-neptun" in context:
        return "tno"
    if "across" in context:
        return "across"
    if "nea" in context or "near earth" in context:
        return "nea"
    return "mba"


def _star_mag(parts: list[str]) -> float | None:
    # Preston Star blocks carry catalog magnitudes immediately after RA/Dec.
    # The middle value is treated as the operational G/V-like choice when present.
    for index in (4, 3, 5):
        if index < len(parts):
            value = _float(parts[index])
            if value is not None and -5 < value < 40:
                return value
    return None


def _star_coordinates(parts: list[str]) -> tuple[str | None, str | None]:
    # Preston stores RA in decimal hours and Dec in degrees. Prefer the apparent
    # coordinate pair later in the Star block, then fall back to the first pair.
    for ra_index, dec_index in ((9, 10), (1, 2)):
        if dec_index >= len(parts):
            continue
        ra = _float(parts[ra_index])
        dec = _float(parts[dec_index])
        if ra is not None and dec is not None and 0 <= ra <= 24 and -90 <= dec <= 90:
            return parts[ra_index], parts[dec_index]
    return None, None


def parse_iota_xml(path: Path, xml_bytes: bytes | None = None) -> list[OccultationEvent]:
    root = ET.fromstring(xml_bytes) if xml_bytes is not None else ET.parse(path).getroot()
    if root.tag != "Occultations":
        raise ValueError(f"Raiz XML no soportada en {path}: {root.tag}")
    return list(_events(root.findall("Event"), path))


def _events(nodes: Iterable[ET.Element], path: Path) -> Iterable[OccultationEvent]:
    for node in nodes:
        element_parts = _parts(node.findtext("Elements"))
        earth_parts = _parts(node.findtext("Earth"))
        star_parts = _parts(node.findtext("Star"))
        object_parts = _parts(node.findtext("Object"))
        orbit_parts = _parts(node.findtext("Orbit"))
        errors_parts = _parts(node.findtext("Errors"))
        id_parts = _parts(node.findtext("ID"))
        number = object_parts[0] if object_parts else ""
        name = object_parts[1] if len(object_parts) > 1 else ""
        ra, dec = _star_coordinates(star_parts)

        # The XML does not label the duration slot. Preserve all Object fields
        # until a source contract maps it unambiguously.
        extra = {
            "elements_fields": element_parts,
            "earth_fields": earth_parts,
            "star_fields": star_parts,
            "object_fields": object_parts,
            "orbit_fields": orbit_parts,
            "errors_fields": errors_parts,
            "id_fields": id_parts,
            "object_number": number or None,
            "object_mag": _float(object_parts[2]) if len(object_parts) > 2 else None,
            "diameter_km": _float(object_parts[3]) if len(object_parts) > 3 else None,
            "max_duration_status": "n/i_unmapped_object_field",
        }
        yield OccultationEvent(
            object_name=f"({number}) {name}".strip() if number or name else None,
            object_type=_object_type(object_parts),
            utc_datetime=_datetime_from_elements(element_parts),
            star_name=star_parts[0] if star_parts else None,
            star_mag=_star_mag(star_parts),
            max_duration_s=None,
            ra=ra,
            dec=dec,
            source=_source_for(path),
            source_file=str(path),
            raw_id=id_parts[0] if id_parts else None,
            raw_line=ET.tostring(node, encoding="unicode"),
            extra=extra,
        )
