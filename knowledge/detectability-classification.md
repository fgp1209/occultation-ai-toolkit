# Detectabilidad y clasificación

## Detectabilidad

No depende solo de la magnitud. Depende de caída esperada, magnitud combinada, ruido real, exposición, número de muestras, fondo, altura, Luna, estabilidad y continuidad temporal.

Prueba preferida: usar una secuencia comparable o el baseline real e inyectar una caída con profundidad y duración previstas; ejecutar el mismo pipeline y medir su recuperación. Los umbrales instrumentales son priors hasta validarlos empíricamente.

`muestras esperadas = duración / exposición` orienta, pero no sustituye la simulación porque ignora fase subframe, integración y ruido correlacionado.

## Prueba empírica

Una prueba defendible conserva:

- serie de ruido y tramo usado;
- cámara, óptica, banda y configuración;
- magnitud, altura, fondo, Luna y condiciones comparables;
- profundidad y duración inyectadas;
- fase de la caída dentro de la cadencia cuando sea relevante;
- pipeline y parámetros de recuperación;
- criterio de detección/falso positivo;
- tasa de recuperación y limitaciones.

No inyectar solo una señal perfectamente alineada con frames. En eventos breves, variar la fase subframe porque la integración puede repartir la señal entre muestras.

## Biblioteca de capacidad

Conservar secuencias estables sin evento permite construir una biblioteca empírica del sistema. Debe cubrir configuraciones y condiciones distintas y registrar dispersión, outliers, correlación temporal y evento mínimo recuperable. Esta biblioteca sustituye progresivamente los límites genéricos por evidencia local.

No extrapolar una prueba entre cámaras, filtros, binning, ganancia, alturas o fondos incompatibles sin declarar la inferencia.

## Ruido temporal

Dos curvas con igual desviación estándar no tienen necesariamente igual detectabilidad. Si el ruido permanece correlacionado durante varios frames, una excursión sostenida es menos excepcional que bajo ruido independiente.

En casos marginales:

1. inspeccionar tendencia y comparaciones;
2. estimar autocorrelación o una escala temporal equivalente;
3. comprobar qué modelo de ruido usa la simulación;
4. repetir con ruido compatible cuando la herramienta lo permita;
5. degradar la confianza si el resultado depende de asumir independencia no demostrada.

## Clasificación

### Positiva

Caída compatible con predicción, presente en el objetivo y no en controles; campo, ventana y timing defendibles; D/R e incertidumbres estimables.

La compatibilidad temporal con la predicción aporta contexto, no permiso para mover D/R o escoger el pipeline que encaje mejor.

### Negativa válida

No aparece caída y se demuestra que una señal prevista habría sido recuperable. Requiere campo correcto, ventana completa, continuidad, timing y sensibilidad suficientes.

Distinguir `negativa válida` de `negativa geométricamente constrictiva`: la segunda, además, limita de forma útil el contorno o la solución combinada. Una estación demasiado alejada puede producir una negativa válida de escaso valor geométrico.

### No concluyente

Falta evidencia o existe un fallo capaz de ocultar o simular el evento: campo dudoso, nube, tracking, saturación, hueco temporal, cadencia insuficiente o señal no detectable.

## Casos frágiles

Un único punto bajo necesita análisis de falso positivo, comparaciones, ruido temporal, integración y corroboración externa. Una negativa cercana al limbo puede ser muy informativa, pero solo después de acreditar detectabilidad.

Una observación con una caída real pero D/R limitados por gaps puede seguir siendo positiva; debe ensancharse la incertidumbre. Una evidencia local insuficiente puede anotarse como compatible con un evento multiestación, sin promocionarla a detección autónoma.

## Salida mínima de clasificación

Registrar:

`clase | evidencia a favor | alternativas examinadas | controles | dependencia externa | limitaciones | estado`

Usar lenguaje proporcional: `observado`, `medido`, `inferido`, `compatible con`, `candidato` o `confirmado`.
