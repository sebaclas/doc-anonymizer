## 1. Implementación de Purga de Metadatos Core

- [x] 1.1 Modificar `anonymize_docx` en `replacer.py` para vaciar y sobreescribir los atributos de `doc.core_properties` (author, last_modified_by, comments, etc.).

## 2. Aplanado de Hipervínculos

- [x] 2.1 Escribir lógica extra dentro del `_deep_replace_xml` (o un paso pre-reemplazo en `anonymize_docx`) que busque bloques `<w:hyperlink>` e independice sus `run` de lectura, destruyendo la etiqueta `w:hyperlink`.
- [x] 2.2 Modificar `docx_extractor.py` para asegurar que el texto expuesto en los hipervínculos esté disponible para Regex sin que los sub-nodos XML fragmenten las cadenas de texto (concatenar strings de links).

## 3. Limpieza de Control de Cambios (Aceptar todos los cambios)

- [x] 3.1 Añadir rutina pre-reemplazo en `anonymize_docx` para simular "Aceptar Cambios": buscar nodos de texto eliminado (`<w:del>`) destruuyéndolos completamente del archivo XML.
- [x] 3.2 Completar la simulación "Aceptar Cambios": confirmar y aplanar todas las adiciones (`<w:ins>`), eliminando su rastro y envoltura para integrarlas al cuerpo ordinario.

## 4. Cobertura de Componentes Auxiliares

- [x] 4.1 Modificar `anonymize_docx` para iterar `doc.part.related_parts` o abrir archivos `.xml` secundarios para aplicar `_deep_replace_xml` al text-flow de Footnotes, Endnotes y Comments.
- [x] 4.2 Actualizar `docx_extractor.py` y `deanonymize_docx` para replicar esta iterabilidad sobre partes adicionales en la lectura e inyección de datos.

## 5. Validación de Hermeticidad

- [x] 5.1 Redactar y añadir archivo de pruebas unitarias que simule un caso con metadatos reales, control de cambios pendientes e hipervínculos de email reales.
- [x] 5.2 Validar que el archivo de salida abre nativamente sin alertas de corrupción del XML y carece de las 4 fugas.
