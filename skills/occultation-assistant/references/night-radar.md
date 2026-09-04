# Radar y selección operativa

## Objetivo

Decidir si merece observar y cuál es la mejor jugada, no producir un catálogo de eventos.

## Flujo de investigación

1. Resolver el intervalo solicitado y sus límites UTC/locales con la zona horaria del perfil. En radar semanal, usar lunes–domingo y vigilar los eventos próximos a medianoche.
2. Consultar primero las fuentes accesibles y comprobar fecha, versión y actualizaciones.
3. Cribar por valor científico y viabilidad aparente sin analizar exhaustivamente eventos mediocres.
4. Aplicar el filtro instrumental y descartar lo que ya sea defendible.
5. Para los candidatos supervivientes, obtener geometría y duración topocéntricas, detectabilidad, campo, timing, meteo y coste operativo.
6. Si falta un dato no accesible, usar [manual-data-acquisition.md](manual-data-acquisition.md). Dar al usuario URL, evento, estación/coordenadas, intervalo, pasos y artefacto exactos; no pedirle que repita el cribado.
7. Reanudar desde el punto bloqueado al recibir cada archivo. No volver a solicitar información ya aportada.
8. Emitir decisión final o `PENDIENTE_DE_DATOS` con el único dato que aún puede cambiarla.

Orden inicial de interés: campañas especiales; TNO/Centauros/Troyanos; objetivos de misión o defensa planetaria; NEA/PHA/ACROSS; binarios o candidatos; eventos brillantes, profundos o largos; geometrías donde la estación aporte una cuerda útil. El interés científico no anula la inviabilidad técnica.

## Pantallazo inicial de OccultWatcher

1. Comprobar primero la meteorología de la estación y la ventana temporal.
2. Leer la captura completa.
3. Pedir `Event.html` solo para candidatos capaces de cambiar la decisión: main posibles, secundarios captables, verdes razonables, blancos excelentes o cercanos y rojos próximos con señal suficiente.
4. Ordenar por fecha y hora local.
5. No tratar el color como calidad: representa geometría/posición de sombra, no detectabilidad instrumental.
6. Confirmar dentro/fuera únicamente con estación, marcador o circunstancias locales.

## Filtro técnico provisional

Sin una matriz instrumental validada, no fijar un límite universal de magnitud. Evaluar conjuntamente:

- magnitud combinada;
- caída esperada y nearby stars;
- duración;
- exposición y muestras durante el evento;
- altura, horizonte y Luna;
- geometría local, probabilidad e incertidumbre;
- estabilidad temporal y continuidad de frames;
- coste de montaje, desplazamiento y sueño;
- valor científico de la estación.

Calcular `muestras_evento = duración / exposición`. Interpretación inicial: ≥10 robusto; 5–10 usable; 2–5 frágil; <2 normalmente insuficiente. No usar estos cortes como prueba de detectabilidad.

Altura inicial: >30° favorable; 20–30° usable; 15–20° penalización fuerte; <15° normalmente descarte. Requiere corrección por horizonte local.

## Prioridad científica

Una negativa puede ser valiosa si restringe el limbo, pero solo es válida si la caída prevista habría sido detectable y la ventana/campo/timing son correctos. Campañas TNO/Centauro, objetos pequeños o geometrías de borde pueden justificar mayor esfuerzo; no justifican una captura incapaz de medir la señal.

## Fuentes

Prioridad: CALL4OBS y campañas oficiales; OccultWatcher/OWC y circunstancias locales; Lucky Star; ACROSS/objetivos de misión; MPC MPES/NEOCP; JPL Horizons/Scout/CNEOS; ESA NEOCC; Gaia/SIMBAD/VizieR cuando haya que validar estrella o entorno; SODIS como contexto histórico; AAVSO/BAA, CALL o Exoplanet Watch para planes alternativos; meteorología local antes del veredicto.

Registrar fuente, fecha de consulta y versión de predicción. Si una fuente no es accesible, declararlo.

## Salida

### Preselección

`Hora local | Evento | Mag | Altura | Color/posición | Calidad preliminar | Pedir HTML | Motivo`

### Decisión final

`Evento | Hora local | Mag combinada | Caída | Duración | Altura | Geometría local | Meteo | Detectabilidad | Decisión | Motivo`

Cerrar con: montar sí/no; evento principal; ventana; configuración inicial; dato pendiente que podría cambiar la decisión; acciones que no compensan.

### Radar semanal

Cuando el usuario pida una semana completa, estructurar el resultado en:

1. resumen ejecutivo y mejor jugada;
2. eventos recomendados A/B y solo los C relevantes;
3. tabla rápida y decisión por noche/tramo;
4. descartes significativos, no el catálogo completo;
5. cambios verificables desde la semana anterior y veredicto operativo.

Si no existe una referencia histórica verificable, declarar que no pueden afirmarse cambios. No rellenar esa sección con inferencias.
