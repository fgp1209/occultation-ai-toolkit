# Skill local: filtrado de ocultaciones

1. Si ya existe un JSON reciente para misma ubicación+ventana, usarlo sin re-leer raw.
2. Si no existe JSON actualizado, ejecutar `python occultations/run.py ...`.
3. Nunca inventar geometría local: si falta, mantener `pending_validation`.
4. Separar análisis de ciencia y operatividad en campos independientes.
5. Marcar explícitamente eventos subsegundo como riesgo operativo.
6. Priorizar TNO/centauro/cubewano/dwarf planet/NEA.
7. MBA subsegundo => práctica técnica salvo caso especial.
8. No recomendar desplazamiento sin geometría local favorable o valor científico alto.
9. Para **eventos futuros** aplicar siempre doble validación:
   - interna: pipeline local asteroidal+lunar sobre raws/cachés disponibles;
   - externa: contraste web independiente con fuentes de ocultaciones fiables.
10. Informe final obligatorio con matriz:
   `Evento | Fuente externa | Pipeline local | Diagnóstico | Fiabilidad`.
11. Si una fuente externa fiable publica un evento y el pipeline no lo detecta, no cerrar como OK: diagnosticar causa raíz.
