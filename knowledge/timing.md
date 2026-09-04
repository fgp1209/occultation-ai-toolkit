# Tiempo y timestamps

## Magnitudes distintas

- **UTC:** escala civil usada habitualmente para reportar.
- **TAI/TT/TDB/UT1:** escalas astronómicas o dinámicas; no son intercambiables con UTC.
- **Exposición:** intervalo durante el cual el sensor integra fotones.
- **Timestamp:** etiqueta asignada por hardware o software a alguna etapa de la captura.
- **Offset:** sesgo sistemático respecto a una referencia.
- **Jitter:** variación del error entre muestras.

## Cadena que debe reconstruirse

`referencia temporal → reloj del sistema/dispositivo → orden de exposición → lectura/transporte → escritura del timestamp → contenedor`.

Preguntas mínimas:

1. ¿Qué fuente disciplina el tiempo: VTI, GPS/PPS, NTP u otra?
2. ¿El timestamp representa inicio, centro, final o recepción del frame?
3. ¿Existe latencia conocida o solo no corregida?
4. ¿Los timestamps son monotónicos y compatibles con la exposición?
5. ¿Hay frames perdidos, duplicados o intervalos anómalos?

## Reglas

- No reconstruir tiempos mediante `número de frame / FPS` cuando existen timestamps reales.
- `delay = 0` significa que no se aplicó corrección; no demuestra latencia cero.
- El centro de exposición puede calcularse desde el inicio solo si la semántica y duración están confirmadas.
- Un dropped frame es una discontinuidad temporal potencialmente geométrica, especialmente junto a D/R.
- Precisión declarada y exactitud calibrada son propiedades distintas.

También separar:

- resolución numérica del timestamp;
- resolución temporal de la exposición;
- exactitud respecto a UTC;
- repetibilidad del offset;
- fiabilidad del sistema bajo la configuración real.

Un timestamp con muchos decimales no localiza D/R con esa precisión si la exposición, el modelo del borde o un gap dominan la incertidumbre.

## Validación de la cadena

La validación más fuerte introduce una referencia conocida por el dominio óptico para que atraviese cámara, driver, captura y archivo. Ejemplos: flash gobernado por PPS/GNSS o comparación simultánea con una cadena previamente caracterizada.

Para cada señal de referencia puede medirse:

```text
delta_t = tiempo_registrado − tiempo_referencia
```

Conservar media o mediana, dispersión, outliers, estabilidad y dependencia con exposición, ROI, FPS, software o carga. Aplicar una corrección solo si el offset está demostrado, es estable y queda documentado. Cero significa `sin corrección aplicada` cuando no existe caracterización.

Revalidar después de cambios de cámara, driver, firmware, software, ordenador, cableado o modo de captura.

NTP puede disciplinar el reloj y mejorar logs; no demuestra por sí solo qué instante de la exposición recibió cada frame.

## Integración y borde

Cuando D/R cae dentro de una exposición, el frame contiene una mezcla de niveles. Inferir una posición subframe requiere semántica temporal, duración, respuesta del detector, dead time y niveles base/oculto defendibles. No redondear automáticamente el borde al centro del frame.

Mantener separados:

- índice del frame;
- timestamp almacenado;
- intervalo físico de exposición;
- estimación de D/R;
- intervalo de incertidumbre.

## Gaps y dropped frames

Calcular:

```text
delta_t[i] = timestamp[i+1] − timestamp[i]
```

Examinar distribución, mediana, dispersión, duplicados y máximo gap. Comparar contra exposición, cadencia esperada y logs.

Si falta información cerca de D/R:

- conservar el patrón real de muestras;
- tratar el borde como un intervalo posible;
- ensanchar incertidumbre;
- no interpolar puntos para inferencia;
- declarar el impacto.

Interpolar para visualización es admisible solo si los puntos sintéticos están identificados y excluidos del análisis.

## Auditoría mínima

Examinar diferencias entre timestamps consecutivos, distribución de intervalos, cambios alrededor del evento, coherencia con `CameraSettings` y log de sincronización. Documentar cualquier corrección sin sobrescribir los tiempos originales.

Salida recomendada:

`fuente | timestamp representa | corrección aplicada | evidencia de exactitud | jitter | gaps | impacto en D/R | estado`
