# Datos mínimos y procedencia

Pide únicamente información capaz de cambiar la decisión o el reporte. Antes de pedirla, comprueba si ya aparece en los archivos aportados.

Cuando el dato dependa de una fuente externa, seguir [manual-data-acquisition.md](manual-data-acquisition.md): indicar el bloqueo, la URL directa, los valores concretos que debe introducir el usuario y el archivo/captura/columnas exactos que debe devolver. No usar peticiones genéricas ni solicitar material de candidatos ya descartados.

## Radar

- Perfil: estación aproximada, zona horaria, equipo, horizonte y límites validados.
- Predicción: objeto, estrella, fecha/hora UTC, versión, magnitudes, caída, duración, geometría e incertidumbre.
- Circunstancias locales: estación seleccionada, altura, azimut, hora local, distancia a central, offset, sigma/probabilidad, mapa y nearby stars.
- Meteorología: capas de nubes y tendencia alrededor del evento; seeing, humedad, viento y Luna cuando alteren viabilidad.

## Captura

- vídeo original y nombre;
- `CameraSettings.txt` o equivalente;
- exposición, ganancia, offset, ROI, binning, formato y FPS real;
- software/cámara;
- fuente temporal y semántica del timestamp;
- inicio/fin, timestamps consecutivos y dropped frames;
- log de sincronización si existe.

## Campo y detectabilidad

- predicción/carta y estrella objetivo;
- orientación/paridad y confirmación independiente del campo;
- objetivo, comparaciones y fondo;
- saturación/linealidad, SNR y estabilidad;
- caída esperada frente al ruido y número de muestras.
- en casos marginales: serie de baseline, fase subframe considerada, prueba de inyección/recuperación, criterio de falso positivo y estructura temporal del ruido.

## Reducción y reporte

- CSV de PyMovie;
- curvas general, objetivo y controles;
- AOTA Report y capturas Tab 4/5;
- `.dat` de Occult/AOTA si se generó;
- plantilla TXT/JOA/OccultWatcher si corresponde;
- datos exactos de estación, observador e instrumento;
- lista de archivos que se adjuntarán.
- método de tracking, apertura/máscara, fondo, normalización, filtros, frames excluidos y motivo;
- modelo de transición/ruido, intervalo de confianza y dependencia de corroboración externa cuando proceda.

## Regla de procedencia

Para cada campo de salida conservar:

`campo | valor | unidad/escala | archivo fuente | método | estado | advertencia`
