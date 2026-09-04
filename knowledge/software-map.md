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

## Funciones que no deben confundirse

- **Extracción:** convierte píxeles en series de objetivo, comparaciones y fondo.
- **Análisis temporal:** estima D/R e incertidumbres sobre una curva ya extraída.
- **Falso positivo:** cuantifica si el ruido puede producir una excursión comparable.
- **Detectabilidad:** prueba si una señal hipotética sería recuperable en ruido representativo.
- **Reporte:** empaqueta resultados y evidencia para revisión.

Una herramienta puede cubrir varias funciones, pero cada salida conserva los supuestos y sesgos de su entrada. AOTA no vuelve independiente una curva sesgada por Tangra; PyOTE no demuestra campo ni timing porque su estadística sea convincente.

## Comparación de pipelines

PyMovie/PyOTE y Tangra/AOTA pueden usarse como análisis de sensibilidad. Antes de comparar resultados, alinear target, frames, timestamps físicos, exposición, baseline y definición de normalización. La discrepancia es un diagnóstico, no una votación.

Guardar proyectos o configuraciones nativas cuando permitan reproducir aperturas, tracking y exclusiones. Las interfaces y formatos concretos se verifican siempre contra la versión oficial vigente.

Al enseñar cualquier herramienta usar: problema → entrada → algoritmo → supuestos → decisiones → salida → controles → fallos.
