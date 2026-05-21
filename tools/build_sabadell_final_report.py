#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

PENDING = "Geometria local pendiente de validacion en mapa interactivo Lucky Star / OccultWatcher Cloud"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye informe editorial semanal de Sabadell.")
    parser.add_argument("--week-json", required=True)
    parser.add_argument("--horizon-json", required=True)
    parser.add_argument("--lunar-json")
    parser.add_argument("--lunar-external-json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--previous")
    return parser.parse_args()


def build(
    week: dict,
    horizon: dict,
    lunar: dict | None = None,
    previous: dict | None = None,
    lunar_external: dict | None = None,
) -> str:
    events = sorted(week["events"], key=lambda event: (-event["score_total"], event["local_datetime"]))
    horizon_events = sorted(horizon["events"], key=lambda event: event["local_datetime"])
    special_types = {"tno", "centaur", "cubewano", "dwarf_planet", "special"}
    high_value = [event for event in events if event.get("object_type") in special_types]
    horizon_nea = [event for event in horizon_events if event.get("object_type") in {"nea", "across"}]
    from_local = datetime.fromisoformat(week["window"]["from_local"])
    to_local = datetime.fromisoformat(week["window"]["to_local"])
    lines = [
        "# Calendario semanal de ocultaciones - Sabadell",
        "",
        f"Ventana: {from_local.isoformat()} - {to_local.isoformat()}  ",
        f"Hora local Sabadell: {week['site']['timezone']}",
        "",
        "## Resumen ejecutivo",
        "",
        f"- Numero de eventos reales detectados por el scorer semanal: {week['summary']['total_events']}.",
        f"- Eventos que pasan filtros observacionales: {week['summary']['observable_events']}.",
        f"- Eventos recomendables operativos: {week['summary']['recommended_events']}.",
        f"- Prioridad operativa semanal: {week['summary']['operational_priority']}.",
        f"- TNOs, centauros, cubewanos, dwarf planets o Special Events en semana: {'si' if high_value else 'no indicados en los eventos filtrados'}.",
        f"- NEA/ACROSS en horizonte 30 dias filtrado: {'si' if horizon_nea else 'no indicados'}.",
        f"- Ocultaciones lunares visibles calculadas: {lunar['summary']['visible_events'] if lunar else 'no calculadas'}.",
        "- La geometria local queda pendiente si no puede validarse desde fuente estatica.",
        "- No se recomienda desplazamiento sin geometria local favorable.",
        "",
        "## Ocultaciones asteroidales",
        "",
        "## Eventos recomendados",
        "",
    ]
    recommended = [event for event in events if event.get("recommendation") == "recommended"]
    if not recommended:
        lines.append("No hay eventos operativos recomendados con geometria local validada.")
    else:
        for event in recommended[:10]:
            lines.append(f"- {event.get('object_name') or 'n/i'} ({event.get('score_total')}/10)")
    lines += ["", "## Eventos de seguimiento", ""]
    editorial_events = [event for event in events if event.get("recommendation") in {"pending_geometry", "follow_up"}][:10]
    if not editorial_events:
        lines.append("No hay seguimientos destacados en esta ventana.")
    for index, event in enumerate(editorial_events, start=1):
        local = datetime.fromisoformat(event["local_datetime"])
        lines += [
            f"### {index}. {event.get('object_name') or 'n/i'}",
            "",
            f"1. Nombre objeto: {event.get('object_name') or 'n/i'}",
            f"2. Fecha local: {local.date().isoformat()}",
            f"3. Hora local Sabadell: {local.strftime('%H:%M:%S')}",
            f"4. Hora UTC: {event.get('utc_datetime') or 'n/i'}",
            f"5. Tipo: {event.get('object_type') or 'n/i'}",
            f"6. Estrella: {event.get('star_name') or 'n/i'}",
            f"7. Magnitud estrella: {_fmt(event.get('star_mag'))}",
            f"8. Caida esperada: {_fmt(event.get('mag_drop'))}",
            f"9. Duracion maxima: {_fmt(event.get('max_duration_s'))}",
            f"10. Incertidumbre: {_extra(event, 'errors_fields')}",
            f"11. Luna/separacion lunar: {_fmt(event.get('moon_sep_deg'))}",
            f"12. Altura desde Sabadell calculada con Astropy: {_fmt(event.get('altitude_deg'))}",
            f"13. Valor cientifico: {_science(event)}",
            f"14. Operatividad desde Sabadell: {_operational(event)}",
            f"15. Dentro/fuera de sombra: {_geometry(event, 'inside_shadow')}",
            f"16. Distancia a linea central: {_geometry(event, 'central_line_distance_km')}",
            f"17. Duracion local esperada: {_geometry(event, 'local_duration_s')}",
            f"18. Probabilidad local: {_geometry(event, 'local_probability')}",
            f"19. Zona Sabadell: {PENDING}",
            f"20. Dificultad observacional: {_difficulty(event)}",
            "21. Necesidad de desplazamiento: no evaluable salvo geometria validada",
            f"22. Fuente / enlace: {event.get('source_url') or event.get('source_file') or 'n/i'}",
            f"23. Score final con motivo: {event.get('score_total')}/10; {_reasons(event)}",
            "",
        ]
    lines += [
        "## Tabla rapida",
        "",
        "| Fecha local | Hora | Objeto | Tipo | Estrella | Mag | Duracion | Altura | Ciencia | Operativa Sabadell | Score |",
        "|---|---:|---|---|---|---:|---:|---:|---|---|---:|",
    ]
    for event in events[:25]:
        local = datetime.fromisoformat(event["local_datetime"])
        lines.append(
            f"| {local.date().isoformat()} | {local.strftime('%H:%M')} | {event.get('object_name') or 'n/i'} | {event.get('object_type') or 'n/i'} | {event.get('star_name') or 'n/i'} | {_fmt(event.get('star_mag'))} | {_fmt(event.get('max_duration_s'))} | {_fmt(event.get('altitude_deg'))} | {_science(event)} | {_operational(event)} | {event.get('score_total')}/10 |"
        )
    lines += ["", "## Descartados", "", "| Evento | Motivo |", "|---|---|"]
    for discarded in week["discarded"][:50]:
        lines.append(f"| {discarded.get('event') or 'n/i'} | {discarded.get('reason') or 'datos incompletos'} |")
    lines += [
        "",
        "## Calendario 30 dias",
        "",
        "| Fecha local | Evento | Tipo | Valor | Estado |",
        "|---|---|---|---|---|",
    ]
    for event in horizon_events[:50]:
        local = datetime.fromisoformat(event["local_datetime"])
        lines.append(f"| {local.date().isoformat()} {local.strftime('%H:%M')} | {event.get('object_name') or 'n/i'} | {event.get('object_type') or 'n/i'} | {_science(event)} | {event.get('recommendation') or 'follow_up'} |")
    lines += [
        "",
        "## Scoring 1-10",
        "",
        "| Score | Evento | Importancia cientifica | Operatividad Sabadell | Motivo |",
        "|---:|---|---|---|---|",
    ]
    for event in events[:25]:
        lines.append(f"| {event.get('score_total')}/10 | {event.get('object_name') or 'n/i'} | {_science(event)} | {_operational(event)} | {_reasons(event)} |")
    lines += ["", "## Cambios desde la semana anterior", ""]
    if previous is None:
        lines.append("Sin informe anterior disponible para comparacion.")
    else:
        lines.append("Comparacion pendiente de revision editorial.")
    lines += ["", "## Ocultaciones lunares", ""]
    lines.extend(_lunar_section(lunar))
    lines += ["", "## Ocultaciones lunares - fuente externa", ""]
    lines.extend(_lunar_external_section(lunar_external))
    return "\n".join(lines) + "\n"


def _fmt(value) -> str:
    return "n/i" if value is None or value == "" else f"{value:.2f}" if isinstance(value, float) else str(value)


def _extra(event: dict, field: str) -> str:
    value = (event.get("extra") or {}).get(field)
    return ", ".join(value) if value else "n/i"


def _geometry(event: dict, field: str) -> str:
    return _fmt((event.get("geometry") or {}).get(field))


def _science(event: dict) -> str:
    return f"{event.get('score_science')}/10 ({event.get('object_type') or 'n/i'})"


def _operational(event: dict) -> str:
    return f"{event.get('score_operational')}/10 ({event.get('recommendation') or 'follow_up'})"


def _difficulty(event: dict) -> str:
    mag = event.get("star_mag")
    if mag is None:
        return "datos incompletos"
    if mag <= 8:
        return "muy favorable por magnitud"
    if mag <= 10:
        return "favorable por magnitud"
    if mag <= 11:
        return "moderada por magnitud"
    return "dificil por magnitud"


def _reasons(event: dict) -> str:
    reasons = (event.get("reason") or []) + (event.get("risks") or [])
    return "; ".join(reasons) if reasons else "sin motivo adicional"


def _lunar_section(lunar: dict | None) -> list[str]:
    if lunar is None:
        return ["Calculo lunar no adjuntado a este informe.", ""]
    lines = [
        f"- Fuente/candidato: {lunar['source']['catalog']}",
        f"- Calculo: {lunar['source']['calculation']}",
        f"- Candidatas estelares evaluadas: {lunar['summary']['candidate_stars']}",
        f"- Eventos lunares visibles encontrados: {lunar['summary']['visible_events']}",
        "",
    ]
    if not lunar["events"]:
        return lines + ["No se encontraron ocultaciones lunares visibles en la ventana.", ""]
    lines += [
        "| Hora local | Estrella | Mag G | Fenomeno | Altura lunar | Fase iluminada | Score lunar | Utilidad |",
        "|---|---|---:|---|---:|---:|---:|---|",
    ]
    for event in lunar["events"]:
        lines.append(
            f"| {event.get('local_datetime') or 'n/i'} | {event.get('star_name') or 'n/i'} | {_fmt(event.get('star_mag'))} | {event.get('event_type') or 'n/i'} | {_fmt(event.get('moon_altitude_deg'))} | {_fmt(event.get('moon_illuminated_fraction'))} | {event.get('score_lunar') or 'n/i'}/10 | {event.get('utility') or 'n/i'} |"
        )
    lines += ["", "Limitaciones lunares:"]
    lines.extend(f"- {item}" for item in lunar.get("limitations", []))
    lines.append("")
    return lines


def _lunar_external_section(lunar_external: dict | None) -> list[str]:
    if lunar_external is None:
        return ["Sin capa externa lunar adjunta en este informe.", ""]
    event = lunar_external.get("event") or {}
    return [
        f"- Evento externo confirmado: {event.get('name') or 'ocultacion lunar brillante (pendiente de detalle)'}",
        f"- Fuente fiable: {lunar_external.get('source_name') or 'n/i'}",
        f"- Enlace fuente: {lunar_external.get('source_url') or 'n/i'}",
        f"- Estado en pipeline lunar local: {lunar_external.get('pipeline_status') or 'no detectado por cobertura/catalogo'}",
        "- Fiabilidad fuente externa lunar: alta (existencia del evento).",
        "- Tiempos exactos para Sabadell: pendientes de predictor topocentrico.",
        "- Fiabilidad pipeline lunar local: baja hasta calcular esta ocultacion con catalogo/cobertura adecuados.",
        "- Clasificacion operativa: evento principal practico de la noche.",
        "- Asteroidales: secundarios de seguimiento/practica pending_geometry.",
        "",
    ]


def main() -> int:
    args = parse_args()
    week = json.loads(Path(args.week_json).read_text(encoding="utf-8"))
    horizon = json.loads(Path(args.horizon_json).read_text(encoding="utf-8"))
    lunar = json.loads(Path(args.lunar_json).read_text(encoding="utf-8")) if args.lunar_json else None
    lunar_external = json.loads(Path(args.lunar_external_json).read_text(encoding="utf-8")) if args.lunar_external_json else None
    previous = json.loads(Path(args.previous).read_text(encoding="utf-8")) if args.previous else None
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(week, horizon, lunar, previous, lunar_external), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
