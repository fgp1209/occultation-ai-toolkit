# Fotometría de vídeo de ocultaciones

El objetivo es estimar flujo temporal con controles suficientes para distinguir ocultación, transparencia, tracking y ruido instrumental.

## Componentes

- **Objetivo:** estrella ocultada, posiblemente mezclada con el cuerpo y estrellas cercanas.
- **Comparaciones:** estrellas no variables, no saturadas y estables durante toda la secuencia.
- **Fondo:** estimación del cielo y señales aditivas locales.
- **Apertura/máscara:** regla que asigna píxeles a fuente y fondo.

## Decisiones con efecto científico

- Apertura grande: añade fondo y contaminantes.
- Apertura pequeña: pierde flujo con seeing, deriva o viento.
- Tracking dependiente del objetivo: puede fallar justo durante la desaparición.
- Normalización: puede eliminar tendencias comunes, pero también deformar la señal si la referencia es inestable.
- Binning temporal: aumenta SNR a costa de resolución y modifica los bordes observados.
- Saturación o no linealidad: invalida razones de flujo aunque la estrella se vea bien.

## Controles

Inspeccionar objetivo, al menos una comparación y fondo antes/durante/después. Una caída simultánea sugiere nube, deriva, fallo de tracking o artefacto común. Comparar extracciones alternativas cuando una decisión de apertura cambie D/R o clasificación.

## Muestreo

Cada frame integra el flujo durante un intervalo; no es una medida instantánea. Exposiciones comparables a la duración suavizan la caída y pueden convertir un evento real en uno o pocos puntos parciales.
