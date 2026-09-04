# Onboarding del observador

## Cuándo ejecutarlo

Ejecutar solo si no existe un perfil confirmado o si el perfil carece de datos necesarios para la tarea. No bloquear una consulta conceptual que no dependa de estación o equipo.

## Datos iniciales

Solicitar en un único bloque compacto:

1. Estación: elegir Observatori de Sabadell u otra; para otra, nombre, coordenadas aproximadas, altitud y zona horaria.
2. Equipo: telescopio/óptica, montura, cámara y software de captura.
3. Tiempo: fuente temporal y qué representa el timestamp, si se conoce.
4. Límites comprobados: magnitud/exposición, altura u horizonte; admitir `desconocido`.
5. Operación: desplazamiento, tiempo de montaje y si debe ponderarse sueño/logística.

No exigir coordenadas exactas para radar. Para reporte, solicitarlas cuando correspondan al lugar real del instrumento.

## Elegir persistencia

Detectar las capacidades de la plataforma y usar una de estas rutas:

### Proyecto con archivos editables

Crear `profiles/local.md` a partir de `profiles/PROFILE_TEMPLATE.md`. Confirmar ruta y contenido guardado. El archivo está excluido de Git.

### GPT, Gem, Claude Project o equivalente

Generar `observer-profile.md` como archivo descargable. Indicar que debe añadirse a los archivos/conocimiento del asistente. No afirmar que quedó instalado hasta que el usuario o la plataforma lo confirme.

### Chat normal con memoria

Pedir autorización explícita antes de guardar datos estables. Guardar solo estación general, equipo, software, preferencias operativas y límites instrumentales confirmados. No guardar coordenadas residenciales exactas, archivos de evento ni resultados científicos en memoria. Si no hay memoria o no se autoriza, generar `observer-profile.md`.

## Confirmación final

Mostrar un resumen corto y marcar cada valor como `CONFIRMADO` o `DESCONOCIDO`. Preguntar solo por errores, no volver a abrir todo el formulario.

Prioridad posterior: archivo local/adjunto → settings del asistente → memoria confirmada → perfil base elegido.
