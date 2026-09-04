# Instrumentación y adquisición

La configuración correcta maximiza información temporal defendible. No existe una exposición, ganancia, FPS o ROI universal: cada elección depende del evento, el sistema real y las condiciones.

## Del fotón al dato

```text
flujo en banda efectiva
→ fotoelectrones
→ carga del píxel
→ lectura electrónica
→ conversión digital
→ frame y metadatos
```

Mantener separados:

- QE y respuesta espectral;
- electrones y ADU;
- control de ganancia del driver y conversión física;
- full well, saturación digital y rango lineal;
- offset/bias y señal astronómica.

Una imagen visible o estética no acredita linealidad. Para fotometría, objetivo y comparaciones deben permanecer dentro del régimen caracterizado del detector.

## Presupuesto de señal y ruido

Una aproximación CCD para una apertura de `n_pix` es:

```text
SNR = señal_fuente /
      sqrt(señal_fuente + n_pix × (fondo + dark + ruido_lectura²))
```

Calcular en electrones cuando se use este modelo. Añadir conceptualmente centelleo, errores de fondo, deriva, transparencia y ruido correlacionado cuando dominen; la ecuación elemental no los absorbe por arte de magia.

En alta cadencia, exposiciones cortas pueden hacer dominante el ruido de lectura. Con fondo alto o aperturas grandes puede dominar el cielo. Con estrellas brillantes y exposiciones cortas puede dominar el centelleo.

## Exposición, cadencia y ciclo

- **Exposición:** intervalo de integración de cada frame.
- **Cadencia:** separación efectiva entre medidas.
- **Dead time:** tiempo no integrado.
- **Duty cycle:** fracción del ciclo durante la que se recogen fotones.
- **FPS efectivo:** propiedad medida de la secuencia, no solo un ajuste nominal.

No asumir `FPS = 1/exposición`. Lectura, interfaz, buffer, almacenamiento y software pueden introducir tiempo muerto o irregularidad.

Reducir exposición mejora resolución temporal, pero disminuye señal por frame y puede aumentar la influencia del ruido de lectura. Aumentarla mejora señal, pero integra y suaviza los bordes. La variable objetivo es la incertidumbre científica útil, no el FPS máximo.

Si la velocidad proyectada es `v`, elegir una resolución temporal cuyo error espacial `v × error_temporal` sea razonable frente a forma, coordenadas, posición estelar y objetivo científico. Más FPS no aporta valor si destruye detectabilidad sin reducir el error dominante.

## ROI, binning y almacenamiento

Una ROI debe conservar:

- objetivo;
- comparaciones suficientes;
- región de fondo representativa;
- margen de deriva;
- patrón que permita recuperar o demostrar el campo.

Reducir ROI puede aumentar la cadencia, pero también eliminar controles o volver frágil el seguimiento. El binning puede mejorar el régimen de lectura o la detectabilidad según la cámara, a costa de muestreo espacial; debe probarse, no presuponerse.

Antes de un evento crítico, ejecutar una captura de duración igual o superior a la prevista y medir FPS efectivo, duty cycle si puede obtenerse, espacio, temperatura, deriva, jitter y gaps.

## Ganancia, gamma y procesamiento

Caracterizar ganancia mediante series comparables. Revisar simultáneamente ruido, rango lineal, saturación, señal y cadencia. En cámaras científicas con datos lineales, conservar linealidad es la opción preferida.

Gamma, reducción digital de ruido, smoothing, filtros recursivos, denoise temporal, estabilización o interpolación pueden deformar una discontinuidad:

- suavizar o desplazar D/R;
- crear colas;
- alterar profundidad;
- correlacionar muestras;
- fabricar una transición gradual.

Conservar el stream más crudo posible y documentar cualquier transformación irreversible. Un filtro espacial que no mezcle frames puede probarse contra una extracción sin filtro; un filtro temporal requiere una justificación y validación mucho más fuertes.

## Configuración mediante prueba A/B

Cuando se dude entre dos configuraciones:

1. usar la misma estrella o una condición comparable;
2. registrar todos los ajustes y la banda efectiva;
3. medir señal, fondo, dispersión, pico y linealidad;
4. medir cadencia, gaps y estabilidad;
5. inyectar o evaluar una caída representativa;
6. comparar detectabilidad y resolución temporal;
7. conservar la evidencia y el régimen de validez.

Etiquetar cada límite como `PRIOR`, `MEDIDO`, `VALIDADO` o `NO_APLICA`. Un umbral histórico deja de gobernar cuando existe caracterización reproducible del sistema actual.

## Matriz de capacidad instrumental

Una matriz útil registra por configuración:

`fecha | cámara/óptica | banda | altura | cielo/Luna | magnitud | caída simulada | exposición | ganancia | ROI/binning | FPS efectivo | duty | SNR | linealidad | deriva | gaps | detectabilidad`

Debe cubrir más de una noche y varios regímenes. Su producto no es una magnitud límite única, sino una capacidad condicionada por profundidad, duración, ruido y configuración.

## Criterios de fallo

La captura queda comprometida si no puede demostrarse alguno de estos puntos cuando afecta al resultado:

- target y comparaciones dentro de campo;
- ausencia de saturación relevante;
- exposición/cadencia suficientes;
- continuidad temporal;
- fuente y semántica del timestamp;
- configuración reconstruible;
- original preservado.

