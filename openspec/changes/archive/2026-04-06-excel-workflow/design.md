## Context

Se ha propuesto permitir que la revisión de entidades detectadas ocurra asincrónicamente con la ayuda de un documento `.xlsx` generado automáticamente. El flujo actual pide input por terminal `s/n/e` frenando el procesamiento general y no permitiendo corregir en caso de error, lo cual es ineficiente en documentos masivos o en empresas segmentadas en áreas de cumplimiento y operación.

## Goals / Non-Goals

**Goals:**
- Generar un archivo Excel con columnas predefinidas y estilizadas.
- Proveer pistas visuales sobre el "status" real de las entidades (e.g. verde cuando ya está auto-aprobada por la BD local).
- Ingestar el Excel completo de decisión.

**Non-Goals:**
- No se abandonará la interfaz CLI (`Rich`), simplemente es un flujo alternativo completo.

## Decisions

- **Estructura del Excel**: Contará con columnas fijas `[Original, Tipo, Pseudonimo, Accion, Origen]`.
- **Acciones y Semántica**: Para que el parser identifique lo que quiere hacer el usuario, aprovechará la convención existente: `s` (Sí/Reemplazar), `n` (No/Ignorar), `e` (Editar).
- **Indicadores Visuales**: `openpyxl` aplicará estilos `PatternFill` verde en aquellas filas provenientes del matcher de DB, mejorando la distinción visual de los "nuevos" vs "conocidos". 
- **Guia de uso**: Se incluirá una hoja de instrucciones dentro del Excel para guiar al usuario en el uso del mismo.    

## Risks / Trade-offs

- [Validación Humana] Un humano puede corromper el Excel metiendo carácteres erróneos o modificando las cabeceras provocando un fallo en el pipeline. -> Mitigación: Validar la existencia estricta de las cabeceras requeridas. Ignorar filas malformadas dando warnings o default fallbacks a "n".
