from __future__ import annotations

import json
from pathlib import Path

PENDING_TEXT = "Geometria local pendiente de validacion en mapa interactivo Lucky Star / OccultWatcher Cloud."


def write_reports(payload: dict, out_base: Path) -> tuple[Path, Path]:
    out_base.parent.mkdir(parents=True, exist_ok=True)
    json_path = out_base.with_suffix(".json")
    md_path = out_base.with_suffix(".md")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Calendario de ocultaciones - {payload['site']['name']}",
        "",
        "## Ventana analizada",
        f"- Inicio local: {payload['window']['from_local']}",
        f"- Fin local: {payload['window']['to_local']}",
        f"- Zona horaria: {payload['site']['timezone']}",
        f"- Fuente raw: {', '.join(payload['sources'])}",
        "- Script usado: occultations/run.py",
        f"- Fecha de generacion: {payload['generated_at']}",
        "",
        "## Resumen ejecutivo",
        f"- Total de eventos procesados: {payload['summary']['total_events']}",
        f"- Eventos observables: {payload['summary'].get('observable_events', len(payload['events']))}",
        f"- Eventos recomendados operativos: {payload['summary'].get('recommended_events', 0)}",
        f"- Prioridad operativa: {payload['summary'].get('operational_priority', 'n/i')}",
        "",
        "## Tabla rapida",
        "",
        "| Fecha local | Hora | Objeto | Tipo | Estrella | Mag | Duracion | Altura | Ciencia | Operativa | Score | Estado |",
        "|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for event in payload["events"]:
        local = event.get("local_datetime", "").split("T")
        lines.append(
            "| {date} | {hour} | {object} | {otype} | {star} | {mag} | {dur} | {alt} | {science} | {operational} | {score} | {rec} |".format(
                date=local[0] if local else "",
                hour=local[1][:5] if len(local) > 1 else "",
                object=event.get("object_name") or "",
                otype=event.get("object_type") or "",
                star=event.get("star_name") or "",
                mag=_fmt(event.get("star_mag")),
                dur=_fmt(event.get("max_duration_s")),
                alt=_fmt(event.get("altitude_deg")),
                science=_fmt(event.get("score_science")),
                operational=_fmt(event.get("score_operational")),
                score=_fmt(event.get("score_total")),
                rec=event.get("recommendation") or "",
            )
        )
    lines += ["", "## Geometria"]
    lines.append(f"- {PENDING_TEXT}")
    lines += ["", "## Descartados", "", "| Evento | Motivo |", "|---|---|"]
    for discarded in payload.get("discarded", [])[:200]:
        lines.append(f"| {discarded.get('event') or 'n/i'} | {discarded.get('reason') or 'n/i'} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def _fmt(value) -> str:
    if value is None or value == "":
        return "n/i"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)
