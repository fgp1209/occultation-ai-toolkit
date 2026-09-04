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

## Después del envío

El dato puede ser revisado, combinado con otras cuerdas, exportado a herramientas de modelado y reanalizado. Por eso deben preservarse decisiones intermedias y no solo una captura de la gráfica.

La documentación interna de SODIS no se redistribuye desde este repositorio. Los usuarios autorizados deben obtenerla mediante la comunidad correspondiente.
