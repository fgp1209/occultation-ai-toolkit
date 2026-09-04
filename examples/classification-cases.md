# Casos didácticos de clasificación

Estos casos describen relaciones lógicas, no eventos reales. No reutilizar sus conclusiones sin comprobar todos los datos del evento actual.

## A — Positiva defendible

- Campo confirmado por WCS.
- Ventana y timestamps continuos.
- Caída solo en el objetivo.
- Comparaciones y fondo estables.
- D/R estables ante cambios razonables de apertura y regiones.

Conclusión posible: `POSITIVA`, con incertidumbre y limitaciones declaradas.

## B — Curva plana y negativa válida

- Campo, ventana y timing confirmados.
- Señal prevista inyectada en el baseline y recuperada con el mismo pipeline.
- No existe caída real ni hueco temporal capaz de ocultarla.

Conclusión posible: `NEGATIVA VÁLIDA`.

## C — Curva plana no concluyente

- Campo plausible pero no demostrado.
- Caída prevista comparable al ruido o a una sola integración.
- No existe prueba de recuperación.

Conclusión: `NO CONCLUYENTE`, no negativa.

## D — Punto bajo aislado

- Un solo punto bajo en el objetivo.
- Deben evaluarse comparaciones, fondo, tracking, timestamps, ruido correlacionado, fase subframe y falso positivo.

Conclusión: no clasificar como positiva solo por apariencia.

## E — Pipelines discrepantes

- Dos extracciones del mismo vídeo producen D/R o clasificación diferentes.
- La discrepancia revela sensibilidad a aperturas, tracking, fondo, filtros o modelo.

Conclusión: localizar la decisión causal; no resolver por mayoría ni elegir el resultado esperado.
