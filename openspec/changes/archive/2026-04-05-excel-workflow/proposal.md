## Why

Para entornos en donde el proceso de anonimización necesita ser validado asíncronamente por otras áreas (como Compliance o Legales), la interacción sincrónica por consola (flujo interactivo `s/n/e`) presenta limitaciones. Permitir que el sistema exporte una grilla de decisión a un archivo Excel (.xlsx) y más tarde la ingiera para procesar el documento mejora drásticamente el modelo colaborativo.

## What Changes

- Modificación del comando `anonymize detect` para exportar también un `.xlsx` configurado para revisión e input del usuario.
- El Excel tendrá una estructura de columnas diseñada: `Original`, `Tipo`, `Pseudonimo`, `Accion`, `Origen`.
- Configuración de formato en Excel (`openpyxl`) para pintar aquellas filas que provienen de la BD en verde claro de manera visual.
- Soporte en el comando `anonymize apply` para parsear este Excel "enriquecido" y realizar el documento final respetando la voluntad de cada fila (`s/n/e`).

## Capabilities

### New Capabilities
- `excel-workflow`: Exportación de entidades a Excel para curaduría asíncrona por parte del usuario, incluyendo validación visual de entidades conocidas e ingesta del archivo terminado.

### Modified Capabilities

## Impact

- Central en la operativa, introduce una mejor experiencia de usuario.
- Refina el uso acual de `openpyxl` incorporando validaciones de celda y formatting.
