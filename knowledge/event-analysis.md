# Inferencia de D/R e incertidumbre

## Modelo básico

La curva ideal tiene un nivel fuera de ocultación, un nivel ocultado y dos transiciones: desaparición D y reaparición R. La observación añade integración temporal, ruido, centelleo, fondo, deriva y posible difracción o diámetro estelar.

## Selección de regiones

Usar baseline suficiente antes y después y datos suficientes en el nivel ocultado. No estrechar regiones para forzar el contacto esperado. Registrar exclusiones con causa observable.

## Transición

Una transición de un frame puede ser adecuada si el borde físico no está resuelto. Modelos más largos requieren evidencia de transición gradual; no deben elegirse solo porque ajusten visualmente mejor.

## Monte Carlo

Monte Carlo genera realizaciones bajo un modelo de señal y ruido para propagar incertidumbre hacia D/R. No implica necesariamente cadenas de Markov. El resultado depende de que el modelo de ruido sea razonable.

Si existe autocorrelación, remuestrear puntos como independientes puede subestimar incertidumbre. Examinar residuos y estabilidad al cambiar regiones, apertura, fondo y parámetros.

## Controles

- repetir ajustes;
- contrastar D/R en tiempo y frame;
- verificar `D < R` y duración;
- revisar dropped frames próximos;
- comparar pipelines como prueba de sensibilidad, no como votación;
- degradar la conclusión si pequeñas decisiones cambian la clasificación.
