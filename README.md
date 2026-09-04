# Occultation AI Toolkit

**V0.1-alpha** — paquete de contexto multiplataforma para ocultaciones estelares.

Sirve para poner a ChatGPT, Claude, Gemini o un agente compatible al día en dos tareas:

- seleccionar y preparar observaciones;
- reducir una captura con PyMovie/AOTA y preparar o auditar el paquete para SODIS.

No envía informes ni sustituye la revisión científica humana.

## Uso inmediato

Pasa esta URL a la IA:

`https://github.com/fgp1209/occultation-ai-toolkit`

Y escribe:

> Lee `AI_START_HERE.md` y sigue sus instrucciones. Después te pasaré los archivos del evento.

La IA debe cargar solo los documentos correspondientes a la tarea y pedir únicamente los datos que puedan cambiar el resultado.

## Perfil base y perfiles privados

El perfil público de referencia es el **Observatori de Sabadell**. Sus coordenadas son operativas para radar, no deben copiarse a un reporte SODIS sin confirmar la estación real de observación.

Para otra estación o equipo existen cuatro opciones:

1. Crear `profiles/local.md` dentro de la carpeta local del proyecto en ChatGPT Work.
2. Copiar `profiles/PROFILE_TEMPLATE.md`, completarlo y adjuntarlo al chat cuando sea necesario.
3. Subir el perfil como archivo de conocimiento de un GPT/Gem/Project personalizado.
4. Guardar los datos estables en las instrucciones o memoria de ese asistente.

Un perfil proporcionado por el usuario prevalece sobre el perfil base. Los datos científicos del evento nunca se recuperan de memoria si existen archivos originales.

## GPT personalizado

Sube estos archivos como conocimiento:

- `AI_START_HERE.md`
- `skills/occultation-assistant/SKILL.md`
- todos los archivos de `skills/occultation-assistant/references/`
- `profiles/observatori-sabadell.md` o el perfil privado correspondiente

Usa como instrucciones el contenido de `CUSTOM_GPT_INSTRUCTIONS.md`.

## Estado alfa

Incluido:

- radar y selección operativa;
- inventario mínimo de datos;
- flujo SER → PyMovie → AOTA → borrador/paquete SODIS;
- auditoría de coherencia y trazabilidad;
- método causal para aprender software astronómico.

Fuera de alcance en V0.1:

- envío automático a SODIS;
- garantía de geometría local sin `Event.html` o circunstancias locales;
- automatización madura de Tangra/PyOTE;
- publicación de manuales de terceros.

## Licencia y fuentes

El repositorio contiene conocimiento operativo sintetizado. Los manuales oficiales de PyMovie, Occult/AOTA, SharpCap y SODIS deben obtenerse de sus distribuidores o comunidades correspondientes. La documentación oficial vigente prevalece cuando cambien interfaces, formatos o reglas de reporte.
