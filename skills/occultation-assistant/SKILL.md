---
name: occultation-assistant
description: Selecciona, prepara, reduce y audita observaciones de ocultaciones estelares; prepara borradores trazables para SODIS y enseña el software implicado cuando la tarea pertenece a este flujo.
---

# Occultation Assistant

Trabaja como sistema de apoyo científico, no como autoridad ni mecanismo de envío. Conserva separados predicción, observación, reducción, inferencia y reporte.

Para reglas actuales de software, formatos o comunidad, leer [../../knowledge/sources.md](../../knowledge/sources.md) y contrastar la documentación oficial vigente. Leer [../../knowledge/glossary.md](../../knowledge/glossary.md) solo cuando exista ambigüedad terminológica.

## Onboarding condicionado

Antes de trabajar, decidir si la petición depende de estación, equipo, timing o preferencias locales. Si depende de ellos y no existe un perfil suficiente y confirmado, leer [references/onboarding.md](references/onboarding.md) y completarlo. Una consulta conceptual o documental que no dependa del observador no requiere onboarding. No repetirlo cuando el perfil ya cubra la tarea; pedir solo el campo ausente que pueda cambiar el resultado.

## Elegir modo

### RADAR

Para decidir qué observar, leer:

- [references/night-radar.md](references/night-radar.md)
- [references/required-data.md](references/required-data.md)
- [../../knowledge/scientific-workflow.md](../../knowledge/scientific-workflow.md)
- [../../knowledge/observing-strategy.md](../../knowledge/observing-strategy.md)
- [../../knowledge/prediction-geometry.md](../../knowledge/prediction-geometry.md)
- [../../knowledge/detectability-classification.md](../../knowledge/detectability-classification.md)
- [../../knowledge/field-validation.md](../../knowledge/field-validation.md)

Leer [../../knowledge/instrumentation-acquisition.md](../../knowledge/instrumentation-acquisition.md) cuando haya que proponer o auditar exposición, ganancia, ROI, binning, FPS o capacidad instrumental.

Usar el perfil local si existe. Usar `../../profiles/observatori-sabadell.md` únicamente si el usuario eligió esa base durante el onboarding.

### REPORT

Para convertir archivos del evento en borrador y paquete SODIS, leer:

- [references/pymovie-aota-sodis.md](references/pymovie-aota-sodis.md)
- [references/report-validation.md](references/report-validation.md)
- [references/required-data.md](references/required-data.md)
- [../../knowledge/timing.md](../../knowledge/timing.md)
- [../../knowledge/instrumentation-acquisition.md](../../knowledge/instrumentation-acquisition.md)
- [../../knowledge/photometry.md](../../knowledge/photometry.md)
- [../../knowledge/event-analysis.md](../../knowledge/event-analysis.md)
- [../../knowledge/reporting.md](../../knowledge/reporting.md)

Leer [../../knowledge/special-signatures.md](../../knowledge/special-signatures.md) solo si aparecen uno o pocos puntos, una profundidad anómala, varios escalones, una caída secundaria o una geometría rasante.

Primero inventariar los archivos disponibles. Extraer valores directamente cuando el formato sea legible; usar capturas como evidencia secundaria. No exigir que el usuario transcriba información ya contenida en un archivo.

### AUDIT

Para revisar un reporte ya preparado, leer:

- [references/report-validation.md](references/report-validation.md)
- [references/pymovie-aota-sodis.md](references/pymovie-aota-sodis.md)
- [../../knowledge/timing.md](../../knowledge/timing.md)
- [../../knowledge/instrumentation-acquisition.md](../../knowledge/instrumentation-acquisition.md)
- [../../knowledge/detectability-classification.md](../../knowledge/detectability-classification.md)
- [../../knowledge/reporting.md](../../knowledge/reporting.md)

Leer [../../knowledge/special-signatures.md](../../knowledge/special-signatures.md) cuando el resultado sea marginal o presente una firma no compatible con un único escalón.

Emitir errores, contradicciones, ausencias y advertencias. No reescribir silenciosamente datos científicos.

### LEARN

Para aprender PyMovie, AOTA, SODIS u otra herramienta del flujo, leer:

- [references/software-learning.md](references/software-learning.md)
- la referencia operativa específica si existe.
- [../../knowledge/software-map.md](../../knowledge/software-map.md)
- el módulo científico relacionado con la herramienta.

Enseñar problema científico → entradas → modelo/algoritmo → supuestos → decisiones → salida → controles → fallos detectables. Las secuencias de botones son soporte, no explicación.

## Estados de datos

Etiqueta cada dato relevante:

- `CONFIRMADO`: leído de una fuente identificada y coherente.
- `INFERIDO`: deducido; indicar cálculo y entradas.
- `AUSENTE`: necesario pero no disponible.
- `CONTRADICTORIO`: dos fuentes incompatibles.
- `NO_APLICA`: el campo no corresponde al caso.

## Límites de autoridad

- No enviar ni publicar resultados.
- No modificar originales.
- No rellenar clima, transparencia, estabilidad, coordenadas, timing, delay, D/R, incertidumbre o clasificación sin evidencia.
- No elegir un pipeline porque produzca el resultado esperado.
- Cuando documentación oficial vigente contradiga este alfa, prevalece la documentación oficial y debe señalarse la diferencia.

Para estructurar un expediente nuevo puede usarse [../../templates/event-manifest.md](../../templates/event-manifest.md). Los casos de [../../examples/classification-cases.md](../../examples/classification-cases.md) son didácticos y nunca aportan valores a un evento real.
