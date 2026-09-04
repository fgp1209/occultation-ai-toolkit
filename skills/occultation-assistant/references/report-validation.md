# Auditoría previa a SODIS

## Resultado obligatorio

Entregar cuatro bloques:

1. Inventario de archivos.
2. Tabla de trazabilidad `campo | valor | fuente | estado | observación`.
3. Errores bloqueantes y advertencias.
4. Borrador listo para revisión humana, dejando huecos explícitos.

## Controles bloqueantes

- Identidad de objeto, estrella y fecha UT coherente en predicción, AOTA, `.dat` y borrador.
- Estación y coordenadas corresponden al lugar real, no al perfil base por defecto.
- Inicio/fin contienen la ventana prevista con margen suficiente.
- D < R y `duración = R − D` dentro del redondeo.
- Escala UTC explícita para predicción, D/R e inicio/fin.
- Exposición, frames integrados y binning coherentes.
- Herramienta declarada coincide con los productos.
- Timestamps monotónicos; discontinuidades y dropped frames revisados cerca de D/R.
- Incertidumbres presentes y compatibles con cadencia/modelo.
- La caída del target no se reproduce en comparaciones o fondo.
- El archivo original permanece intacto.

## Clasificación

- `POSITIVA`: caída compatible con el evento, controles y timing; D/R defendibles.
- `NEGATIVA VÁLIDA`: no hay caída y se demuestra campo correcto, ventana, timing, continuidad y detectabilidad de la señal prevista.
- `NO CONCLUYENTE`: evidencia insuficiente o fallo capaz de ocultar/simular el evento.

Una curva plana no prueba una negativa. Un evento de una o pocas muestras exige tratamiento explícito y no debe sobreinterpretarse.

## Política de corrección

- Corregir automáticamente solo formato inequívoco, unidades o cálculos derivados, mostrando el cambio.
- No escoger entre fuentes contradictorias sin evidencia adicional.
- No inventar valores para completar el formulario.
- No realizar el envío.

## Cierre

Estado final: `LISTO PARA REVISIÓN`, `BLOQUEADO` o `NO CONCLUYENTE`. Nunca `ENVIADO`.
