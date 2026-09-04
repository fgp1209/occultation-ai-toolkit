# Firmas marginales y especiales

Este módulo se usa cuando la curva no se describe adecuadamente como un único escalón limpio. Su función es mantener hipótesis competidoras abiertas y exigir controles proporcionales a la afirmación.

## Disciplina de lenguaje

Separar:

- `observado`: patrón presente en los datos;
- `medido`: magnitud obtenida con método identificado;
- `inferido`: consecuencia del modelo y sus entradas;
- `compatible con`: hipótesis no exclusiva;
- `candidato`: alternativas principales razonablemente examinadas;
- `confirmado`: conclusión sustentada por revisión o evidencia global suficiente.

No convertir “doble caída” en “satélite”, “caída parcial” en “doble estrella” ni “cuerda corta” en “relieve”.

## Evento de una muestra

Puede ser físico si la duración es menor o comparable a la exposición, D y R caen dentro del mismo intervalo o la cuerda es rasante. También puede ser un outlier.

Antes de clasificar:

- demostrar target, ventana y timing;
- inspeccionar comparaciones y fondo;
- revisar tracking, apertura, hot pixels y defectos;
- comprobar gaps y frames adyacentes;
- identificar filtrado temporal;
- evaluar falso positivo con un modelo de ruido compatible;
- registrar qué aporta una estación independiente.

Si una ocultación de duración `tau` ocurre dentro de una exposición `T`, el frame mezcla ambos estados:

```text
flujo_frame ≈ ((T − tau) × flujo_base + tau × flujo_oculto) / T
```

Una profundidad intermedia puede ser integración subframe; no demuestra ocultación parcial ni multiplicidad.

## Profundidad menor que la prevista

Revisar en orden causal:

1. magnitudes y banda de la predicción;
2. identidad del target y contribución del cuerpo;
3. saturación/linealidad;
4. fondo y contaminantes dentro de la apertura;
5. transparencia mediante comparaciones;
6. integración parcial;
7. estrella doble con una componente no ocultada;
8. diámetro estelar, difracción u otra física relevante.

Expresar también la razón `flujo_evento / flujo_base` cuando sea más informativa que una diferencia de magnitud mal condicionada. Usar cifras significativas acordes con el ruido; una cota puede ser más honesta que tres decimales.

## Estrella doble

Una doble no resuelta puede producir escalones separados o una caída parcial si solo se oculta una componente. En la simplificación sin flujo del cuerpo:

```text
flujo_evento / flujo_base ≈ flujo_componente_visible / flujo_total
```

Antes de elevar la hipótesis, revisar contaminación, integración, fondo, saturación, filtros, ruido correlacionado, estabilidad de apertura, catálogos de dobles y calidad astrométrica. Un evento puede restringir separación proyectada; no proporciona por sí solo una órbita binaria.

## Caída secundaria

Hipótesis mínimas:

- estrella doble;
- satélite;
- graze, relieve o cuerpo bilobulado;
- anillo o estructura difusa si el objeto lo permite;
- nube/transparencia;
- tracking, apertura o fondo;
- gap, jitter o dropped frame;
- filtro temporal;
- ruido o defecto del detector.

Una hipótesis de satélite gana fuerza si la señal es exclusiva del target, sobrevive reducciones razonables y forma una geometría coherente entre estaciones. Mantener `candidato` hasta revisión, repetición o confirmación independiente.

## Graze y borde irregular

Cerca del limbo, una cuerda corta puede producir caída breve, mínimo parcial o varios D/R. La interpretación requiere el sky-plane plot y las demás cuerdas/negativas; una curva aislada no distingue necesariamente relieve, forma bilobulada y cuerpo secundario.

## Física del borde

El perfil observado combina:

- contorno geométrico;
- integración temporal y dead time;
- difracción de Fresnel;
- diámetro angular estelar;
- respuesta espectral;
- ruido y procesamiento.

Escala de Fresnel aproximada:

```text
F = sqrt(longitud_de_onda × distancia / 2)
tiempo_F ≈ F / velocidad_proyectada
```

Solo modelar estructura física fina cuando su escala sea comparable a la resolución de la captura y los artefactos ordinarios estén controlados.

## Árbol de salida

Tras el análisis, usar una salida proporcionada a la evidencia:

- artefacto identificado;
- no concluyente;
- evento marginal local;
- compatible con una hipótesis física;
- candidato dependiente de corroboración;
- detección robusta;
- confirmado por revisión/campaña.

Documentar siempre qué parte procede de la curva local y cuál de otras estaciones, catálogos o modelos.

