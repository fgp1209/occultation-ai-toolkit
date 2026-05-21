# Occultation Skill (local)

## Instalacion
```bash
python -m venv .venv
pip install -r requirements.txt
```

## Ejemplo Sabadell
```bash
python occultations/run.py \
  --from "2026-05-24T21:00:00+02:00" \
  --to "2026-05-25T04:00:00+02:00" \
  --horizon-days 30 \
  --out reports/sabadell-2026-05-24-night
```

Si no existe `settings.local.json`, el primer arranque pide el observatorio base y propone el Observatori de Sabadell:
`41.550111 N`, `2.091453 E`, `224 m`, zona horaria `Europe/Madrid`.
El fichero queda local e ignorado por Git; las siguientes ejecuciones reutilizan ese sitio.

Puedes sobreescribir el sitio desde CLI con `--name`, `--lat`, `--lon`, `--alt` y `--timezone`.

Carpetas y settings locales ignorados: `data/raw/`, `data/cache/`, `reports/`, `settings.local.json`.

Anade raws manualmente en `data/raw/` y ejecuta el script.

Limitaciones:
- No sustituye OccultWatcher.
- La geometria local exacta requiere validacion externa.
- La duracion maxima no equivale a duracion local.
