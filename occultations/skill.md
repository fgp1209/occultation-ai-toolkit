# Skill local: filtrado de ocultaciones

1. Si ya existe un JSON reciente para misma ubicación+ventana, usarlo sin re-leer raw.
2. Si no existe JSON actualizado, ejecutar `python occultations/run.py ...`.
3. Nunca inventar geometría local: si falta, mantener `pending_validation`.
4. Separar análisis de ciencia y operatividad en campos independientes.
5. Marcar explícitamente eventos subsegundo como riesgo operativo.
6. Priorizar TNO/centauro/cubewano/dwarf planet/NEA.
7. MBA subsegundo => práctica técnica salvo caso especial.
8. No recomendar desplazamiento sin geometría local favorable o valor científico alto.
