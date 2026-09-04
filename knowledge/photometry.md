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

## Extracción como experimento

En curvas marginales, variar únicamente una decisión cada vez y registrar:

- método de tracking;
- apertura o máscara;
- región/estimador de fondo;
- comparaciones;
- calibraciones y filtros;
- puntos excluidos y causa;
- dispersión y estructura del baseline;
- profundidad, D/R e incertidumbres resultantes.

No aceptar una apertura por defecto sin inspeccionar PSF, deriva y estabilidad. Una apertura computada o extracción sofisticada puede mejorar el tracking sin mejorar mucho el SNR si domina el centelleo.

El target no debe ser la única referencia posicional durante una desaparición profunda: el centro puede saltar a ruido o a otra fuente. Preferir una transformación del campo, estrellas guía o una máscara cuya posición no dependa del brillo instantáneo del target.

## Modelo de fondo

La sustracción de fondo es un modelo, no un ritual. Una estimación frame a frame añade su propia varianza:

```text
varianza_flujo ≈ varianza_apertura + varianza_fondo_escalado
```

Conservar por separado señal de apertura y canal de fondo. Si la curva es marginal, comparar estimadores razonables: fondo instantáneo, lento o representativo. No fijar un fondo constante cuando hay nubes iluminadas, gradientes, fuentes móviles o cambios instrumentales; tampoco inyectar ruido innecesario desde una región de fondo inestable.

## Comparaciones

Elegir comparaciones no saturadas, estables, con SNR suficiente y sin contaminación. El brillo idéntico no es obligatorio. El color puede importar a baja altura o en secuencias largas por extinción diferencial, especialmente cuando se interpreta una pequeña fracción de flujo residual.

Una comparación demuestra variaciones comunes solo dentro de su propio régimen de calidad. Varias comparaciones permiten distinguir una estrella problemática de una perturbación global.

## Normalización y filtros

La normalización puede retirar tendencias lentas, pero una ventana demasiado corta puede absorber parte de un evento largo. Comparar curva cruda y normalizada y documentar el modelo.

Evitar filtros que mezclen frames. Cualquier smoothing temporal puede alterar bordes, profundidad y autocorrelación. Un filtro espacial debe validarse contra la extracción sin filtro y no elegirse porque produzca la forma esperada.

## Muestreo

Cada frame integra el flujo durante un intervalo; no es una medida instantánea. Exposiciones comparables a la duración suavizan la caída y pueden convertir un evento real en uno o pocos puntos parciales.

## Profundidad

Además de magnitudes, conservar la razón lineal:

```text
q = flujo_evento / flujo_base
fracción_desaparecida = 1 − q
delta_mag = −2.5 log10(q)
```

Si el flujo ocultado está cerca del fondo, `delta_mag` puede estar mal condicionado. Usar cifras significativas compatibles con la incertidumbre y, cuando proceda, una cota en vez de precisión ficticia.

## Criterio entre extracciones

Priorizar:

1. estabilidad y representatividad del baseline;
2. ausencia de artefactos en objetivo, controles y fondo;
3. conservación física de la profundidad;
4. D/R estables ante cambios razonables;
5. incertidumbre y falso positivo compatibles con el ruido.

No elegir por estética, mayor SNR aislado ni cercanía a la predicción.
