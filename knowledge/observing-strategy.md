# Estrategia de observación

El producto del radar es una decisión operativa: qué evento merece recursos, desde qué estación y con qué dato pendiente. El interés del objeto no compensa una cadena incapaz de producir evidencia interpretable.

## Seis puertas de viabilidad

### 1. Geometría local

Confirmar estación, versión, línea/bandas, probabilidad u offset, duración local y valor de la posición. No inferir “dentro” por color, país o mapa regional.

### 2. Detectabilidad medida

Combinar magnitud en banda útil, flujo combinado, caída, duración, exposición, ruido comparable, muestras, saturación y controles. En casos marginales, preferir una prueba de inyección/recuperación.

### 3. Tiempo fiable

Exigir una cadena temporal adecuada al objetivo: fuente, semántica del timestamp, integración, correcciones demostradas, continuidad y régimen previamente validado.

### 4. Campo verificable

Preparar carta/FOV, objetivo, comparaciones, orientación, paridad y margen. Definir una comprobación independiente; GoTo no basta.

### 5. Meteorología

Separar forecast de nowcast. Evaluar nubes por capas y tendencia, transparencia, seeing cuando afecte a SNR, humedad/rocío, viento, Luna y horizonte durante la ventana relevante.

### 6. Coste operativo

Considerar montaje, desplazamiento, coordinación, seguridad, descanso y obligaciones posteriores. Más candidatos no implican más noches útiles.

Un resumen útil del objetivo es:

```text
valor científico esperado × probabilidad de dato válido / coste total
```

No convertirlo en una cifra ficticiamente precisa; sirve para hacer explícitos los factores.

## Clases de decisión

- **Principal:** justifica montar o desplazarse específicamente.
- **Secundario:** compensa si el sistema ya está operativo o comparte tramo.
- **Práctica:** produce caracterización o competencia, sin fingir valor de campaña.
- **Descarte técnico:** no existe una configuración razonable que produzca dato interpretable.
- **Descarte operativo:** sería técnicamente posible, pero no compensa coste, meteo o logística.

Registrar por qué se asigna la clase y qué información podría cambiarla.

## Plan completo

Un candidato promovido debe tener:

- evento, fuente, versión, UTC/local y circunstancias topocéntricas;
- valor esperado de positiva y negativa;
- cartas amplia y de detalle, orientación y confirmación;
- configuración inicial con alternativas y prueba previa;
- cronograma con baseline suficiente;
- almacenamiento, nombres y respaldo;
- contingencias y criterio de aborto.

La configuración es un punto inicial sometido a prueba sobre el campo real.

## Criterios de aborto

Definirlos antes de la ventana. Ejemplos: campo no demostrado, SNR insuficiente, saturación irresoluble, timing no válido, gaps persistentes, deriva que expulsa controles, nubes incompatibles, almacenamiento insuficiente o riesgo físico/logístico.

Cancelar correctamente puede ser el mejor resultado operativo; no equivale a observación ni debe convertirse en negativa.

## Durante la ventana crítica

Reducir carga cognitiva:

1. indicar la acción;
2. indicar la condición de éxito;
3. indicar qué no debe tocarse;
4. registrar incidencias;
5. posponer teoría y optimizaciones no esenciales.

Priorizar continuidad, campo y tiempo. Evitar recentrados, cambios de exposición o ganancia durante la ventana salvo que un fallo evidente vaya a invalidar toda la captura.

## Prepointing y automatización

Prepointing usa la deriva celeste para que el target entre en un campo preparado a la hora prevista. Puede ser útil con objetivos débiles o estaciones móviles, pero exige carta específica, hora, declinación, orientación, escala y una demostración previa. No introducirlo por primera vez en un evento crítico.

La automatización puede apuntar, resolver, centrar, capturar y archivar; no elimina la obligación de demostrar campo, foco, tiempo, continuidad, meteo y espacio. Distinguir siempre entre plate solving para medir la posición y una orden de recentrado que pueda mover la montura durante la captura.

## Cierre de sesión

Comparar previsto con real y registrar:

- cambios de configuración y causa;
- incidencias y consecuencia científica;
- originales, logs, copias y hashes;
- estado provisional, sin sobreclasificar;
- reducción pendiente;
- reparación o prueba que evitará repetir el fallo.

