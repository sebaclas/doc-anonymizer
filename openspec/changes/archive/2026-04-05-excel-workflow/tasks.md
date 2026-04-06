## 1. Detección y Output

- [x] 1.1 Analizar `detect` para que no solo detecte sino que almacene la procedencia de cada hit (`NER`, `DB`, `REGEX`)
- [x] 1.2 Extender el export de detección en `mapping.py` o módulo equivalente para que escriba las cabeceras y los datos (`Original, Tipo, Pseudonimo, Accion, Origen`)

## 2. Formatting de Archivo (openpyxl)

- [x] 2.1 Implementar la lógica condicional en la generación del excel: Si origen == 'DB', aplicar `PatternFill` verde
- [x] 2.2 Autocompletar el campo `Accion` sugerido para Regex y DBs a manera de guía del usuario interactivo (opcional pero preferido)

## 3. Integración en Reemplazo (`apply`)

- [x] 3.1 Actualizar el comando `anonymize apply` para parsear este excel ampliado verificando la robustez de las filas
- [x] 3.2 Modificar el core o la iteración para que al encontrar un `Accion` evalué la convención "s/n/e"
- [x] 3.3 Test manual exportando la deteccion e importando aplicacion de manera full asincrónica
