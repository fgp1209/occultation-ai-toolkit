# Reporte, revisión y archivo

Reportar convierte una medida local en un dato comunitario reutilizable. El formulario es la última representación de la evidencia, no su sustituto.

## Principio de procedencia

Cada campo debe tener valor, unidad/escala, fuente, método, estado y advertencia. Fuentes típicas:

- predicción/Event: objeto, estrella y versión;
- coordenadas confirmadas: estación;
- original/CameraSettings: cámara, exposición, inicio y fin;
- log temporal: fuente y estado de sincronización;
- PyMovie/Tangra: fotometría y controles;
- AOTA/PyOTE: D/R, duración, modelo e incertidumbre;
- registro de sesión: meteorología e incidencias.

## Reglas

- Mantener UTC explícito y separado de hora local.
- No completar clima o calidad de cielo desde recuerdos no registrados.
- No redondear de forma incompatible entre productos.
- Conservar original, CSV/curva, análisis, reporte y logs.
- Marcar campos ausentes o contradictorios.
- Generar borrador y auditoría; el envío requiere revisión humana.

Mantener lenguaje proporcional a la evidencia: una caída puede estar `observada`, una duración `medida`, una causa `inferida`, una firma ser `compatible con` una hipótesis y un objeto quedar como `candidato`. Reservar `confirmado` para evidencia global o revisión suficiente.

## Expediente por capas

### Original y contexto

- vídeo/imágenes originales inmutables;
- hashes y copias;
- predicción/Event y versión;
- coordenadas, datum, método y precisión;
- configuración y logs de adquisición/tiempo.

### Reducción reproducible

- proyecto de extracción cuando exista;
- aperturas, máscaras, tracking, fondo y comparaciones;
- serie numérica con timestamps y flujos;
- frames excluidos y causa;
- curvas de objetivo, controles y fondo.

### Inferencia

- configuración y salida del analizador;
- D/R, duración e intervalos;
- modelo de transición y ruido;
- falso positivo y detectabilidad cuando procedan;
- reducciones alternativas relevantes.

### Reporte y revisión

- borrador y versión finalmente revisada;
- adjuntos exactos;
- correcciones con motivo;
- comunicaciones científicas relevantes del revisor.

Una imagen de la curva no sustituye la serie numérica; una curva compacta no sustituye el original cuando haya que rehacer tracking, fondo o aperturas.

## Coherencia de precisión

- No reportar más decimales de los defendibles.
- D/R no pueden parecer más precisos que exposición, gaps, timing y modelo.
- Una profundidad cercana al fondo puede requerir una cota o razón de flujo.
- Mantener el mismo redondeo y escala temporal entre tabla, reporte y figuras.
- Diferenciar dato ausente de cero físico o corrección no aplicada.

## Después del envío

El dato puede ser revisado, combinado con otras cuerdas, exportado a herramientas de modelado y reanalizado. Por eso deben preservarse decisiones intermedias y no solo una captura de la gráfica.

La documentación interna de SODIS no se redistribuye desde este repositorio. Los usuarios autorizados deben obtenerla mediante la comunidad correspondiente.

Una observación puede ganar valor con nuevas efemérides, catálogos de dobles, modelos de forma o métodos estadísticos. No sobrescribir silenciosamente una reducción histórica: crear una nueva derivación, conservar la anterior y explicar qué evidencia o método cambió.
