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

La elección del solver y la del modelo de ruido son problemas distintos. Un algoritmo puede localizar razonablemente el borde y, aun así, producir intervalos demasiado estrechos si simula ruido blanco donde la curva contiene estructura temporal.

No interpretar automáticamente `±1 sigma` como una distribución normal. Cuando la distribución simulada sea asimétrica o limitada por frames concretos, conservar intervalos o cuantiles y explicar qué los determina.

## Presupuesto de incertidumbre

Identificar contribuciones de:

- duración de exposición e integración subframe;
- cadencia y dead time;
- exactitud, offset y jitter temporal;
- gaps próximos al borde;
- ruido blanco y correlacionado;
- definición de baseline/nivel ocultado;
- apertura, fondo, tracking y normalización;
- diámetro estelar, Fresnel u otra física resuelta;
- modelo de transición.

No es obligatorio combinarlas manualmente si el software ya las modela, pero sí declarar cuáles están incluidas, cuáles no y cuál domina.

## Análisis de pocos puntos

Para uno o dos puntos deprimidos, separar cuatro afirmaciones:

1. el punto es visualmente llamativo;
2. es raro bajo un modelo explícito de ruido;
3. es compatible con predicción e integración;
4. tiene corroboración geométrica independiente.

Cada nivel aporta evidencia diferente. Un test de falso positivo no repara campo, timing o continuidad dudosos.

## Pipelines cruzados

Comparar pipelines descomponiendo:

```text
captura + timestamps + extracción + normalización + modelo temporal + ruido
```

Verificar mismo target, frames, tiempos físicos, exposición y ventanas antes de comparar D/R. Si dos reducciones razonables convergen dentro de incertidumbre, aumenta la robustez. Si discrepan, no promediar: localizar la decisión causal o declarar la discrepancia sin resolver.

## Controles

- repetir ajustes;
- contrastar D/R en tiempo y frame;
- verificar `D < R` y duración;
- revisar dropped frames próximos;
- comparar pipelines como prueba de sensibilidad, no como votación;
- degradar la conclusión si pequeñas decisiones cambian la clasificación.

Añadir cuando corresponda:

- repetir con aperturas y fondos razonables;
- comparar curva cruda y normalizada;
- ejecutar falso positivo/detectabilidad;
- examinar ACF o escala de correlación;
- comprobar si un gap convierte D/R en intervalo;
- consultar el módulo de firmas especiales sin adoptar la hipótesis más llamativa.

## Resultado reproducible

Conservar:

`datos de entrada | frames usados | regiones | exclusiones | modelo | ruido | iteraciones | intervalo | D/R | sensibilidad | limitaciones`
