# Cadena científica de una ocultación

Una ocultación transforma una variación temporal de flujo en una restricción geométrica. El producto científico no es una gráfica aislada, sino una cadena trazable.

## Etapas

1. **Predicción:** trayectoria relativa cuerpo-estrella, incertidumbre, caída y duración esperadas.
2. **Selección:** valor científico frente a detectabilidad, meteorología y coste operativo.
3. **Estación:** posición topocéntrica real; determina la cuerda potencial.
4. **Campo:** identificación independiente de la estrella correcta.
5. **Captura:** secuencia con cadencia, rango dinámico, comparaciones y ventana suficientes.
6. **Tiempo:** relación demostrable entre timestamp almacenado y exposición física.
7. **Fotometría:** píxeles → flujo del objetivo y controles.
8. **Inferencia:** estimación de D/R, duración e incertidumbres bajo un modelo explícito.
9. **Clasificación:** positiva, negativa válida o no concluyente.
10. **Reporte:** datos, procedencia, limitaciones y archivos preservados para revisión.

## Dependencias críticas

- Una reducción perfecta no corrige un campo equivocado.
- Más FPS no compensa SNR insuficiente.
- Un reloj sincronizado no demuestra la semántica física del timestamp.
- Una curva plana no acredita una negativa.
- Dos programas sobre el mismo vídeo no son dos observaciones independientes.
- El reporte no puede ser más preciso que la evidencia original.

## Puertas antes de capturar

Una decisión de observación debe superar o resolver:

1. geometría topocéntrica y valor de la estación;
2. detectabilidad con el sistema y ruido esperados;
3. timing adecuado al error espacial buscado;
4. campo demostrable y estable;
5. meteorología compatible durante la ventana;
6. coste operativo, coordinación y seguridad.

Un fallo técnico en las tres primeras puertas normalmente no se compensa por interés del evento. Una cancelación bien justificada es una decisión válida; no es una observación negativa.

## Flujo iterativo

La cadena no es puramente lineal. Los controles pueden obligar a volver atrás:

- una prueba de SNR cambia exposición o candidato;
- el FOV real cambia ROI o comparaciones;
- un test de continuidad reduce el FPS aceptable;
- una discrepancia de extracción reabre aperturas, fondo o tracking;
- un reviewer puede requerir el original o una derivación nueva.

Cada retorno debe conservar la versión anterior y la razón del cambio.

## Objeto de evidencia

Conservar predicción/versionado, coordenadas, configuración, original intacto, logs temporales, cartas, aperturas, curvas objetivo/control, análisis D/R, incertidumbres, clasificación y paquete reportado.

Separar al menos cuatro capas: original/contexto, reducción reproducible, inferencia y reporte/revisión. El archivo científico debe permitir reconstruir el camino sin depender de memoria del observador.
