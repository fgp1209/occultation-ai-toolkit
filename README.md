# Occultation AI Toolkit

**V0.2-alpha** — paquete de contexto multiplataforma para ocultaciones estelares.

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

Cuando la tarea dependa del observador y falte un perfil, ejecutará un onboarding breve para identificar estación, equipo, timing y forma de persistirlo. Una consulta conceptual no requiere perfil. No debe volver a pedir datos ya guardados y confirmados.

## Perfil base y perfiles privados

El perfil público de referencia es el **Observatori de Sabadell**. Sus coordenadas son operativas para radar, no deben copiarse a un reporte SODIS sin confirmar la estación real de observación.

Para otra estación o equipo existen cuatro opciones:

1. En ChatGPT Work/Codex o un proyecto con archivos editables: crear `profiles/local.md`, ignorado por Git.
2. En un GPT, Gem, Claude Project o equivalente: generar `observer-profile.md` para descargarlo y subirlo a los archivos del asistente.
3. En un chat normal con memoria: guardar únicamente datos estables después de obtener autorización explícita.
4. Sin persistencia: entregar el perfil como archivo para adjuntarlo en futuras sesiones.

Un perfil proporcionado por el usuario prevalece sobre el perfil base. Los datos científicos del evento nunca se recuperan de memoria si existen archivos originales.

## GPT personalizado

Sube estos archivos como conocimiento:

- `AI_START_HERE.md`
- `skills/occultation-assistant/SKILL.md`
- todos los archivos de `skills/occultation-assistant/references/`
- `profiles/observatori-sabadell.md` o el perfil privado correspondiente

Usa como instrucciones el contenido de `CUSTOM_GPT_INSTRUCTIONS.md`.

## Corpus

`knowledge/` contiene conocimiento científico original y destilado. No reproduce los manuales empleados como fuentes. La skill carga módulos diferentes para RADAR, REPORT, AUDIT y LEARN.

## Estado alfa

Incluido:

- radar y selección operativa;
- inventario mínimo de datos;
- flujo SER → PyMovie → AOTA → borrador/paquete SODIS;
- auditoría de coherencia y trazabilidad;
- método causal para aprender software astronómico;
- onboarding y perfil persistente según plataforma;
- corpus modular de tiempo, campo, fotometría, detectabilidad, D/R y reporte;
- predicción/astrometría, adquisición instrumental y estrategia de observación;
- diagnóstico de eventos marginales, dobles, caídas secundarias y geometrías rasantes;
- archivo reproducible y reanálisis posterior.

Fuera de alcance en V0.2:

- envío automático a SODIS;
- garantía de geometría local sin `Event.html` o circunstancias locales;
- automatización madura de Tangra/PyOTE;
- publicación de manuales de terceros.

## Licencia y fuentes

El contenido original se publica bajo CC BY 4.0; consulta `LICENSE`. Los manuales oficiales de PyMovie, Occult/AOTA, SharpCap y SODIS deben obtenerse de sus distribuidores o comunidades correspondientes. La documentación oficial vigente prevalece cuando cambien interfaces, formatos o reglas de reporte.
