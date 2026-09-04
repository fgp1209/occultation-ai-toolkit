# Radar y selección operativa

## Objetivo

Decidir si merece observar y cuál es la mejor jugada, no producir un catálogo de eventos.

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

Prioridad: OccultWatcher/OWC y circunstancias locales; campañas oficiales como Lucky Star; MPC MPES/NEOCP; JPL Scout/CNEOS; ESA NEOCC; AAVSO/BAA, CALL o Exoplanet Watch para planes alternativos; meteorología local al inicio y antes del veredicto.

Registrar fuente, fecha de consulta y versión de predicción. Si una fuente no es accesible, declararlo.

## Salida

### Preselección

`Hora local | Evento | Mag | Altura | Color/posición | Calidad preliminar | Pedir HTML | Motivo`

### Decisión final

`Evento | Hora local | Mag combinada | Caída | Duración | Altura | Geometría local | Meteo | Detectabilidad | Decisión | Motivo`

Cerrar con: montar sí/no; evento principal; ventana; configuración inicial; dato pendiente que podría cambiar la decisión; acciones que no compensan.
