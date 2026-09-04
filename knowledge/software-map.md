# Mapa funcional del software

| Capa | Herramientas habituales | Entrada → salida | Riesgo principal |
|---|---|---|---|
| Predicción/coordinación | Occult4, OccultWatcher/OWC | catálogos y órbitas → evento/circunstancias | confundir mapa regional con geometría local |
| Captura | SharpCap u otro capturador | sensor + configuración → SER/FITS/vídeo | timing, saturación, dropped frames |
| Campo | Cartes du Ciel, ASTAP, plate solving | imagen → WCS/identidad | aceptar GoTo sin verificación |
| Extracción | PyMovie, Tangra | píxeles → curva temporal | tracking, apertura, fondo, filtros |
| Inferencia | AOTA, PyOTE | curva → D/R e incertidumbre | modelo de ruido/transición inadecuado |
| Reporte | Occult/AOTA, SODIS | medida local → registro revisable | campos copiados o escalas mezcladas |

## Relaciones

- PyMovie y Tangra son alternativas de extracción; no prueban independencia si parten del mismo vídeo.
- AOTA está integrado en el ecosistema Occult y recibe curvas para analizar contactos.
- PyOTE combina análisis temporal con funciones específicas como detectabilidad y falso positivo.
- SODIS estructura el reporte europeo y su revisión; no reemplaza la reducción.

Al enseñar cualquier herramienta usar: problema → entrada → algoritmo → supuestos → decisiones → salida → controles → fallos.
