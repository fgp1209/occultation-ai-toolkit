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

## Auditoría mínima

Examinar diferencias entre timestamps consecutivos, distribución de intervalos, cambios alrededor del evento, coherencia con `CameraSettings` y log de sincronización. Documentar cualquier corrección sin sobrescribir los tiempos originales.
