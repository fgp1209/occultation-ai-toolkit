# Detectabilidad y clasificación

## Detectabilidad

No depende solo de la magnitud. Depende de caída esperada, magnitud combinada, ruido real, exposición, número de muestras, fondo, altura, Luna, estabilidad y continuidad temporal.

Prueba preferida: usar una secuencia comparable o el baseline real e inyectar una caída con profundidad y duración previstas; ejecutar el mismo pipeline y medir su recuperación. Los umbrales instrumentales son priors hasta validarlos empíricamente.

`muestras esperadas = duración / exposición` orienta, pero no sustituye la simulación porque ignora fase subframe, integración y ruido correlacionado.

## Clasificación

### Positiva

Caída compatible con predicción, presente en el objetivo y no en controles; campo, ventana y timing defendibles; D/R e incertidumbres estimables.

### Negativa válida

No aparece caída y se demuestra que una señal prevista habría sido recuperable. Requiere campo correcto, ventana completa, continuidad, timing y sensibilidad suficientes.

### No concluyente

Falta evidencia o existe un fallo capaz de ocultar o simular el evento: campo dudoso, nube, tracking, saturación, hueco temporal, cadencia insuficiente o señal no detectable.

## Casos frágiles

Un único punto bajo necesita análisis de falso positivo, comparaciones, ruido temporal, integración y corroboración externa. Una negativa cercana al limbo puede ser muy informativa, pero solo después de acreditar detectabilidad.
