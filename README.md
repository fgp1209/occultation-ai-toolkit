# Occultation Skill (local)

Herramienta local para convertir raw reales de ocultaciones en informes para Sabadell.

## Instalacion

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Flujo real

1. Descarga o copia raw reales en `data/raw/`.

```bash
python tools/download_real_sources.py \
  --from "2026-05-18T00:00:00+02:00" \
  --to "2026-06-17T23:59:59+02:00" \
  --out data/raw/real_occultations_2026-05-18_2026-06-17.csv \
  --download-preston-zips
```

2. Normaliza HTML, CSV y XML compatibles a CSV interno.

```bash
python tools/normalize_raw_sources.py \
  --raw-dir data/raw \
  --from "2026-05-18T00:00:00+02:00" \
  --to "2026-06-17T23:59:59+02:00" \
  --timezone Europe/Madrid \
  --out data/cache/normalized_sabadell_2026-05-18_2026-06-17.csv
```

El normalizador escribe tambien un `*.diagnostic.json` con conteos por fichero, descartes y campos no mapeados. La cache depende de `raw_dir`, hashes de raws, ventana, zona horaria y version del parser.

3. Ejecuta el scorer para la semana y el horizonte 30 dias.

```bash
python occultations/run.py \
  --name "Observatori de Sabadell" \
  --lat 41.548 --lon 2.107 --alt 220 \
  --timezone Europe/Madrid \
  --from "2026-05-18T00:00:00+02:00" \
  --to "2026-05-24T23:59:59+02:00" \
  --input data/cache/normalized_sabadell_2026-05-18_2026-06-17.csv \
  --out reports/sabadell-week-2026-05-18_2026-05-24
```

```bash
python occultations/run.py \
  --name "Observatori de Sabadell" \
  --lat 41.548 --lon 2.107 --alt 220 \
  --timezone Europe/Madrid \
  --from "2026-05-18T00:00:00+02:00" \
  --to "2026-06-17T23:59:59+02:00" \
  --input data/cache/normalized_sabadell_2026-05-18_2026-06-17.csv \
  --out reports/sabadell-30d-2026-05-18_2026-06-17
```

4. Revisa el informe editorial final.

```bash
python tools/build_sabadell_final_report.py \
  --week-json reports/sabadell-week-2026-05-18_2026-05-24.json \
  --horizon-json reports/sabadell-30d-2026-05-18_2026-06-17.json \
  --out reports/sabadell-final-2026-05-18_2026-05-24.md
```

## Flujo lunar

Las ocultaciones lunares se calculan en una capa paralela. El raw estelar sale de Gaia DR3 por TAP para un corredor alrededor de la trayectoria lunar topocentrica; despues Astropy calcula cruces entre esas estrellas y un limbo lunar esferico visto desde el observatorio.

```bash
python tools/download_lunar_sources.py \
  --from "2026-05-24T21:00:00+02:00" \
  --to "2026-05-25T07:00:00+02:00" \
  --out data/raw/lunar/gaia-sabadell-2026-05-24_2026-05-25.csv
```

```bash
python tools/run_lunar_occultations.py \
  --from "2026-05-24T21:00:00+02:00" \
  --to "2026-05-25T07:00:00+02:00" \
  --input data/raw/lunar/gaia-sabadell-2026-05-24_2026-05-25.csv \
  --out reports/sabadell-lunar-2026-05-24_2026-05-25
```

Adjunta el JSON lunar al informe final. La seccion lunar existe siempre; sin `--lunar-json` queda marcada como no calculada.

```bash
python tools/build_sabadell_final_report.py \
  --week-json reports/sabadell-window-2026-05-24_2026-05-25.json \
  --horizon-json reports/sabadell-30d-2026-05-18_2026-06-17.json \
  --lunar-json reports/sabadell-lunar-2026-05-24_2026-05-25.json \
  --out reports/sabadell-final-2026-05-24_2026-05-25.md
```

Si no existe `settings.local.json`, el primer arranque pide el observatorio base y propone el Observatori de Sabadell. El fichero queda local e ignorado por Git. Puedes sobreescribir el sitio desde CLI con `--name`, `--lat`, `--lon`, `--alt` y `--timezone`.

Carpetas y settings locales ignorados: `data/raw/`, `data/cache/`, `reports/`, `settings.local.json`.

## Limitaciones

- No sustituye OccultWatcher.
- La geometria local exacta requiere validacion externa y bloquea recomendaciones operativas.
- El parser XML conserva los campos raw no mapeados en `extra`; no asigna duracion maxima o incertidumbre desde slots Preston no documentados.
- La duracion maxima de una fuente no equivale a duracion local.
- El calculo lunar actual usa Gaia DR3, la efemeride builtin de Astropy y un limbo lunar esferico; sirve para descubrimiento local y practica/timing, no sustituye una reduccion lunar de precision con perfil de limbo.
