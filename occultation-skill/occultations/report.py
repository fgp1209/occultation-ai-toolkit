from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PENDING_TEXT = "Geometría local pendiente de validación en mapa interactivo Lucky Star / OccultWatcher Cloud."


def write_reports(payload: dict, out_base: Path) -> tuple[Path, Path]:
    out_base.parent.mkdir(parents=True, exist_ok=True)
    json_path = out_base.with_suffix(".json")
    md_path = out_base.with_suffix(".md")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# Calendario de ocultaciones — {payload['site']['name']}", "", "## Ventana analizada"]
    lines += [f"- Inicio local: {payload['window']['from_local']}", f"- Fin local: {payload['window']['to_local']}", f"- Zona horaria: {payload['site']['timezone']}", f"- Fuente raw: {', '.join(payload['sources'])}", "- Script usado: occultations/run.py", f"- Fecha de generación: {payload['generated_at']}"]
    lines += ["", "## Resumen ejecutivo", f"- Total de eventos: {payload['summary']['total_events']}"]
    lines += ["", "## Tabla rápida", "", "| Fecha local | Hora | Objeto | Tipo | Estrella | Mag | Duración | Altura | Ciencia | Operativa | Score |", "|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for e in payload["events"]:
        local = e["local_datetime"].split("T") if e.get("local_datetime") else ["",""]
        lines.append(f"| {local[0]} | {local[1][:5]} | {e.get('object_name','')} | {e.get('object_type','')} | {e.get('star_name','')} | {e.get('star_mag')} | {e.get('max_duration_s')} | {e.get('altitude_deg')} | {e.get('score_science')} | {e.get('score_operational')} | {e.get('score_total')} |")
    lines += ["", "## Eventos recomendados"]
    for e in payload["events"]:
        lines += [f"- {e.get('object_name')} ({e.get('recommendation')})", f"  - Geometría local: {PENDING_TEXT if e['geometry']['status']=='pending_validation' else 'Validada'}"]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
