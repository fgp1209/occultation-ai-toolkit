# SER → PyMovie → AOTA → paquete SODIS

Esta referencia describe el flujo probado para vídeo SER. Los nombres de menús pueden cambiar; la documentación oficial vigente prevalece.

## 1. Preservación e inventario

No modificar el SER. Conservar juntos: vídeo, `CameraSettings`, log temporal, predicción/Event image, cartas y productos de reducción. Registrar hashes cuando sea viable.

Antes de reducir comprobar:

- `FrameCount` y `NumTimestamps` coherentes;
- `DateTimeUTC` y primer/último timestamp coherentes con la captura;
- exposición, FPS real y dropped frames;
- qué instante físico representa el timestamp.

## 2. PyMovie

Abrir el SER y ajustar contraste solo para visualización.

Aperturas recomendadas:

- `target`: apertura dinámica sobre la estrella ocultada;
- `track1` y, si existe, `track2`: comparaciones estables durante toda la secuencia;
- `no-star`: apertura estática sobre cielo limpio.

Recorrer frames antes, durante y después del evento. Rechazar comparaciones que salten, saturen o pierdan centro. Guardar el grupo de aperturas antes del análisis.

Analizar la secuencia completa. Comprobar que una caída del objetivo no aparece simultáneamente en comparaciones o fondo. Guardar curva general, curva objetivo y controles; exportar CSV conservando timestamps reales.

## 3. AOTA

Abrir el CSV desde AOTA y asignar `Signal = target`.

Ejecutar `Check Times` y `Check Measures`. No editar frames sin anomalía demostrable. Como configuración inicial para una medida por frame:

```text
Frames/bin = 1
First frame = 0
Normalise to = None
Background = Point by point
```

Seleccionar regiones con baseline suficiente antes/después de D y R y nivel ocultado suficiente. No estrecharlas para forzar contactos.

Para una transición abrupta no resuelta puede partirse de `Transition = 1`. El número de iteraciones Monte Carlo y el intervalo de confianza deben registrarse. Repetir el ajuste y comprobar estabilidad de D/R e incertidumbres.

## 4. Corrección temporal

No copiar configuraciones de cámaras analógicas a un sistema SER digital. Para un SER sin corrección temporal demostrada, partir de:

```text
Camera = SER system
Video system = Other
Frames integrated = 0
```

`Camera delay`, `Exposure delay` y `Time difference` solo pueden fijarse con conocimiento del sistema o caracterización. Cero significa «sin corrección aplicada», no «latencia físicamente nula».

El reporte debe identificar herramienta de medida, escala temporal y cualquier corrección aplicada.

## 5. Productos Occult/AOTA

Guardar:

- imagen del análisis global/Tab 4;
- formulario o ajuste D/R/Tab 5;
- AOTA Report;
- `.dat` mediante `Report the Light Curve`, si procede.

Antes de aceptar el `.dat`, verificar fecha, objeto, estrella, observador y coordenadas. Rechazar archivos accidentales con año/objeto/coordenadas por defecto.

## 6. Borrador SODIS

Mapa mínimo de fuentes:

| Campo | Fuente primaria |
|---|---|
| Objeto, estrella, predicción | Event/OccultWatcher o campaña |
| Estación y coordenadas | perfil científico confirmado del lugar real |
| Inicio/fin | `CameraSettings` o timestamps del original |
| D/R e incertidumbres | AOTA Report |
| Duración | `R − D`, contrastada con reporte |
| Exposición y cámara | `CameraSettings` |
| Fuente temporal | log/configuración temporal |
| SNR | AOTA Report o análisis identificado |
| Clima/comentarios | registro contemporáneo; vacío si no existe |

No rellenar transparencia, estabilidad, clima ni comentarios por inferencia visual. No confundir hora local con UTC.

## 7. Paquete de revisión

1. Predicción/Event image.
2. Curva general PyMovie.
3. Curva objetivo y controles.
4. CSV PyMovie.
5. Imágenes AOTA Tab 4/5.
6. AOTA Report.
7. `.dat`, si existe.
8. Borrador TXT/formulario requerido.
9. `CameraSettings`.
10. Log temporal.

Cadena: `SER intacto → PyMovie → CSV + controles → AOTA → D/R + incertidumbre → .dat/borrador → auditoría → revisión humana`.
