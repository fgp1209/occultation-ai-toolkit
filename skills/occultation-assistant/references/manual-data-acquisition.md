# Adquisición guiada de datos externos

## Principio

La IA debe agotar primero las fuentes que pueda consultar directamente. Después del cribado, solo debe solicitar material manual para candidatos cuya decisión siga abierta o para los que falte una prueba crítica.

No pedir «más datos» de forma genérica ni encargar al usuario una búsqueda completa. Cada solicitud debe ser una acción breve, verificable y ligada a una decisión.

## Ciclo obligatorio

1. Definir estación/perfil, intervalo y objetivo del radar.
2. Consultar las fuentes accesibles y registrar fecha de consulta, versión y limitaciones.
3. Crear una preselección pequeña; descartar técnicamente antes de pedir archivos.
4. Para cada candidato superviviente, separar datos obtenidos, calculados, inferidos y ausentes.
5. Solicitar únicamente el dato ausente que pueda cambiar la decisión.
6. Analizar el archivo recibido antes de solicitar el siguiente.
7. Detener las solicitudes cuando ya pueda emitirse una decisión defendible.

Si varios datos se obtienen en una misma pantalla o archivo, pedirlos juntos. Si pertenecen a sitios o candidatos diferentes, guiar paso a paso para reducir errores.

## Formato de cada solicitud manual

Toda petición debe contener:

- **Bloqueo:** qué decisión no puede cerrarse y por qué.
- **Fuente:** nombre y URL directa.
- **Entrada:** objeto, estación, coordenadas, fecha, intervalo y demás valores que debe introducir el usuario.
- **Acción:** ruta o controles que debe abrir.
- **Entrega:** archivo, captura, tabla o columnas exactas que debe devolver.
- **Criterio de parada:** qué no necesita descargar.
- **Continuación:** qué comprobará la IA al recibirlo.

Ejemplo de forma, no de valores:

> Falta la geometría topocéntrica de la estación; sin ella no puede distinguirse entre observar desde la base o descartar. Abre la fuente y URL indicadas, selecciona el evento, usa la estación/coordenadas proporcionadas y guarda `Event.html`; si la exportación no existe, envía una captura completa de `Local circumstances` y del mapa con el marcador. No descargues datos de los demás eventos. Se comprobarán duración local, distancia a la línea central, sigma, probabilidad, altura y nearby stars.

No remitir al usuario a una portada si existe una URL más directa y estable.

## Recetas por fuente

### OccultWatcher / OccultWatcher Cloud

Fuentes:

- https://cloud.occultwatcher.net/
- https://occultations.org/observing/software/ow/

Cuando la IA no pueda acceder a los detalles locales:

1. Identificar explícitamente el evento y la estación.
2. Pedir `Event.html` del candidato seleccionado.
3. Si no puede guardarse, pedir capturas de la ficha completa, `Local circumstances`, mapa con estación/Home y bandas, y nearby stars/caída efectiva 4"/8" si aparecen.
4. Solicitar que sean visibles hora central, duración local, altura, azimut, distancia/offset, sigma o probabilidad y versión de la predicción.
5. No pedir HTML de descartes técnicos ni de toda la lista.

El color de la fila nunca sustituye estas circunstancias.

### CALL4OBS / campañas IOTA-ES

Fuente: https://call4obs.iota-es.de/

La IA debe revisar directamente las campañas accesibles. Si una ficha o adjunto queda bloqueado:

1. Dar la URL exacta de la campaña.
2. Pedir captura o descarga de la ficha y de los enlaces de predicción vigentes.
3. Solicitar que sean visibles última actualización, motivo científico, comentarios del coordinador y enlace de evento.
4. No tratar la campaña como viable hasta cruzarla con equipo, estación y geometría local.

### Lucky Star

Fuente: https://lesia.obspm.fr/lucky-star/

Si no puede obtenerse la predicción de estación, pedir únicamente el PDF, tabla o captura del evento preseleccionado con:

- cuerpo y estrella;
- fecha y versión;
- mapa y bandas de incertidumbre;
- magnitud y caída;
- closest approach o probabilidad local;
- duración y circunstancias locales, si aparecen.

Indicar las coordenadas aproximadas del perfil que deben usarse en el formulario. No usar coordenadas exactas privadas si las aproximadas bastan para cribar.

### Meteoblue y servicio meteorológico oficial

La IA debe construir la consulta para la estación o punto desplazado real, no asumir Sabadell ni reutilizar la meteo de otra ubicación.

Si la tabla no es accesible, pedir una captura limitada a evento −2 h → evento +2 h donde aparezcan:

- nubes bajas, medias y altas;
- tendencia;
- seeing cuando afecte a detectabilidad;
- humedad, viento y temperatura cuando afecten a rocío o estabilidad;
- Luna;
- horas de salida/puesta relevantes.

Para España, usar AEMET como contraste cuando haya predicción disponible: https://www.aemet.es/

No pedir meteo detallada para eventos ya descartados. A largo plazo, clasificar la meteo como pendiente, no inventarla ni convertirla en descarte definitivo.

### JPL Horizons

Fuente: https://ssd.jpl.nasa.gov/horizons/

Cuando haga falta una verificación topocéntrica, indicar:

- designación exacta del objeto;
- tipo de efeméride;
- coordenadas y altitud de la estación;
- inicio, fin y paso temporal;
- magnitudes o columnas que deben copiarse;
- escala temporal y referencia exigidas.

Pedir la tabla de salida como texto o archivo. Horizons valida efemérides; no sustituye un path de ocultación especializado.

### MPC MPES / NEOCP

Fuentes:

- https://www.minorplanetcenter.net/iau/MPEph/MPEph.html
- https://www.minorplanetcenter.net/iau/NEO/toconfirm_tabular.html

Para MPES, proporcionar objeto, código de observatorio o coordenadas, fecha inicial, número de fechas, paso, formato y columnas requeridas. Solicitar solo las filas que cubran la ventana útil. Una efeméride genérica no confirma la sombra local.

### Gaia Archive, SIMBAD y VizieR

Fuentes:

- https://gea.esac.esa.int/archive/
- https://simbad.cds.unistra.fr/
- https://vizier.cds.unistra.fr/

La IA debe hacer primero la consulta si dispone de acceso. Si necesita intervención manual, entregar el identificador o coordenadas exactas y pedir solo los campos relevantes: identificadores cruzados, época, posición, movimiento propio, magnitudes con banda, duplicidad/binariedad y nearby stars. No solicitar exportaciones completas del catálogo.

### SODIS

Fuente: https://sodis.iota-es.de/

Usarlo para contexto de observaciones y para preparar el reporte, no como predicción actual. Si el acceso requiere sesión, pedir al usuario únicamente la captura o exportación necesaria para el evento o el campo del formulario que se esté auditando. Nunca solicitar credenciales ni ejecutar el envío.

## Fallos de acceso

Si una web requiere sesión, JavaScript, una aplicación local o un formulario que la IA no puede controlar:

- declarar la limitación concreta;
- no fingir que se revisó;
- dar la secuencia manual exacta;
- aceptar `Event.html`, HTML guardado, PDF, captura o texto copiado;
- verificar legibilidad y procedencia al recibirlo.

Si el artefacto no contiene el dato crítico, explicar qué falta y guiar una única recuperación adicional. No reiniciar el proceso ni volver a pedir todo.

## Resultado intermedio

Mientras falten datos manuales, entregar:

- preselección provisional;
- descartes ya defendibles;
- candidato bloqueado;
- una sola tanda mínima de acciones;
- estado `PENDIENTE_DE_DATOS`, nunca una conclusión fabricada.

Tras cada aportación, actualizar la decisión y conservar:

`dato | fuente/URL | fecha de consulta | versión | método | estado | efecto sobre la decisión`
