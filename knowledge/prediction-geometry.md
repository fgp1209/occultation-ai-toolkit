# Predicción, astrometría y geometría

Una predicción de ocultación combina una estrella propagada al instante del evento, una efeméride del cuerpo, un tamaño o modelo de forma, la posición topocéntrica del observador y sus incertidumbres. El mapa es una representación de ese modelo, no una medición del evento futuro.

## Capas que no deben mezclarse

- **Identificador estelar:** etiqueta de catálogo; no es una posición eterna.
- **Posición catalogada:** coordenadas asociadas a un marco y una época.
- **Posición propagada:** incorpora movimiento propio y, cuando corresponde, paralaje y movimiento radial.
- **Posición aparente/observada:** añade transformaciones dependientes del instante y del observador.
- **Efeméride geocéntrica:** posición calculada desde el centro terrestre.
- **Circunstancia topocéntrica:** geometría para una estación concreta.

Registrar catálogo, identificador, época, marco y versión de la predicción cuando estén disponibles. Un identificador UCAC4 puede coexistir con una solución astrométrica basada en Gaia.

## Calidad de la estrella

Gaia mejora radicalmente muchas posiciones, pero no vuelve infalible cada solución. Revisar cuando sea relevante:

- incertidumbres y covarianzas;
- movimiento propio y época;
- RUWE u otros indicadores de ajuste;
- duplicidad, aceleración o fotocentro no modelado;
- diámetro angular estimado;
- correspondencia inequívoca entre catálogos.

Una estrella doble o una solución astrométrica problemática puede desplazar la sombra calculada o alterar la profundidad prevista.

## De error angular a desplazamiento

Para ángulos pequeños:

```text
desplazamiento ≈ distancia × error_angular_en_radianes
```

Por eso milisegundos de arco pueden convertirse en kilómetros en el plano de la sombra. Nunca introducir grados, arcsec o mas directamente en la relación lineal sin convertir a radianes.

## Predicción y versiones

Conservar:

- fuente y fecha de consulta;
- versión o actualización;
- efeméride/orbita identificada cuando conste;
- catálogo o solución estelar;
- diámetro o modelo adoptado;
- línea central, bandas e incertidumbre;
- velocidad, duración y caída;
- circunstancias locales de la estación evaluada.

Comparar dos predicciones como dos modelos versionados. No trasladar automáticamente la geometría de una versión al tiempo, estrella o path de otra.

## Sigma, offset y probabilidad

`Sigma` suele describir una escala de incertidumbre proyectada. No equivale por sí sola a probabilidad local, ni garantiza una distribución gaussiana. La probabilidad de ocultación también depende del diámetro adoptado, la forma, la orientación y la posición de la estación.

Separar siempre:

- distancia u offset respecto a la línea nominal;
- sigma de la predicción;
- probabilidad calculada por la fuente;
- ancho físico del cuerpo o sombra;
- valor científico de una positiva o negativa desde esa estación.

## De tiempos a cuerda

Con velocidad proyectada transversal `v` y duración `R − D`:

```text
longitud_de_cuerda ≈ v × (R − D)
error_espacial_temporal ≈ v × incertidumbre_temporal
```

Una cuerda mide una sección del contorno proyectado, no el diámetro tridimensional ni necesariamente el diámetro medio. Una sola cuerda conserva ambigüedad transversal sobre el centro si no existe información adicional de forma.

## Valor de una estación

El valor geométrico no se ordena solo por cercanía a la central:

- una cuerda central suele restringir extensión;
- una cuerda marginal puede localizar el limbo;
- una negativa validada próxima a una positiva restringe dónde no estaba el contorno;
- una negativa lejana puede aportar poco;
- una estación coordinada puede ser más valiosa que otra con mayor probabilidad aislada.

Una cuerda única bien temporizada puede aportar D/R, longitud, astrometría relativa, control de efeméride y pistas sobre dobles o estructuras secundarias. No reconstruye por sí sola el contorno completo.

## Regímenes distintos

- **Cuerpos pequeños/NEO:** eventos breves, sombras estrechas y posible predominio de la resolución temporal.
- **TNO/Centauros:** estrellas a menudo débiles, campañas coordinadas y mayor relevancia potencial de Fresnel, diámetro estelar, atmósferas o anillos.
- **Objetivos de misión:** el valor puede justificar más esfuerzo, pero nunca relaja campo, timing o detectabilidad.

## Resultado fuera del path

No corregir retrospectivamente la observación para hacerla coincidir con una predicción precisa. Auditar por separado estación, tiempo, campo, D/R, versión, tamaño y forma. Un desplazamiento real puede ser precisamente el dato que mejore la efeméride.

