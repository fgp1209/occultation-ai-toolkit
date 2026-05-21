from __future__ import annotations


def score_event(event: dict) -> tuple[int, int, int, list[str], list[str], str]:
    reasons: list[str] = []
    risks: list[str] = []
    otype = (event.get("object_type") or "").lower()
    science = 3
    if any(k in otype for k in ["tno", "centaur", "cubewano", "dwarf", "special"]):
        science = 9
    elif any(k in otype for k in ["nea", "across", "campaign"]):
        science = 6
    elif "mba" in otype:
        science = 3

    operational = 4
    mag = event.get("star_mag")
    dur = event.get("max_duration_s")
    alt = event.get("altitude_deg")
    sun = event.get("sun_altitude_deg")
    moon = event.get("moon_sep_deg")

    if mag is not None:
        if mag <= 8:
            operational += 3
            reasons.append("Estrella muy favorable")
        elif mag <= 10:
            operational += 2
            reasons.append("Estrella favorable")
        elif mag <= 11:
            operational += 1
            reasons.append("Estrella moderada")
        else:
            operational -= 2
            risks.append("Estrella dificil")
    if dur is not None:
        operational += 2 if dur >= 1 else 1 if dur >= 0.5 else -2
        if dur < 1:
            reasons.append("Evento subsegundo o casi subsegundo")
            if "mba" in otype:
                science = min(science, 3)
    if alt is not None:
        if alt >= 35:
            operational += 2
        elif alt >= 20:
            operational += 1
        else:
            operational -= 3
    if sun is not None and sun > -6:
        operational -= 3
        risks.append("Cielo no suficientemente oscuro")
    if moon is not None:
        if moon < 10:
            operational -= 3
            risks.append("Luna muy cercana")
        elif moon < 20:
            operational -= 1
            risks.append("Luna cercana")

    total = max(1, min(10, round((science + operational) / 2)))
    operational = max(1, min(10, operational))
    pending_geometry = event.get("geometry", {}).get("status") == "pending_validation"
    if pending_geometry:
        recommendation = "pending_geometry" if total >= 5 else "technical_practice"
    else:
        recommendation = "recommended" if total >= 7 else "follow_up" if total >= 5 else "technical_practice"
    return science, operational, total, reasons, risks, recommendation
