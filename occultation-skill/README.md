# Occultation Skill (local)

## Instalación
```bash
python -m venv .venv
pip install -r requirements.txt
```

## Ejemplo Sabadell
```bash
python occultations/run.py \
  --name "Observatori de Sabadell" \
  --lat 41.548 --lon 2.107 --alt 220 \
  --timezone Europe/Madrid \
  --from "2026-05-24T21:00:00+02:00" \
  --to "2026-05-25T04:00:00+02:00" \
  --horizon-days 30 \
  --out reports/sabadell-2026-05-24-night
```

Carpetas locales ignoradas: `data/raw/`, `data/cache/`, `reports/`.

Añade raws manualmente en `data/raw/` y ejecuta el script.

Limitaciones:
- No sustituye OccultWatcher.
- La geometría local exacta requiere validación externa.
- La duración máxima no equivale a duración local.
