## Why

Para garantizar la hermeticidad y fiabilidad del proceso de anonimización en documentos de Microsoft Word (DOCX), necesitamos ir más allá de la limpieza del texto nativo visible (cuerpo del documento, encabezados y pie de página). Actualmente hay un riesgo de fuga de datos en artefactos arquitectónicos estructurados de Word, tales como metadatos nativos (Autor), hipervínculos estructurados con metas en otros archivos (`.rels`), control de cambios y comentarios, los cuales ignoraban parcialmente o totalmente nuestros filtros.

## What Changes

- Sanitización forzosa de **Hipervínculos**: Todos los vínculos serán removidos y convertidos a texto plano para que el regex pueda detectar direcciones e información, y evite que queden destinarios de email en relaciones XML.
- Purga de **Metadatos Core (Propiedades)**: Se borrarán los identificadores del DOCX (Autor, Editado Por, Empresa, etc.).
- Procesamiento de **Comentarios y Notas**: Extracción y reemplazo en `word/comments.xml`, `word/footnotes.xml` y `word/endnotes.xml`.
- Aplanado de **Control de Cambios** (Track Changes): Aceptar definitivamente todos los cambios pendientes en el documento antes del proceso de anonimizado. Consolidará el texto insertado y removerá sin rastro el texto eliminado. (**BREAKING**: El documento final dejará de tener marcas de revisión y quedará aplanado con la versión final del texto).

## Capabilities

### New Capabilities
- `docx-deep-sanitization`: Capacidad transversal enfocada en limpiar paquetes ".rels", purgar propiedades "core.xml", sub-archivos de notas y comentarios en DOCX.

### Modified Capabilities
- `document-processing`: Se expanden las directrices de reemplazo y extracción de texto para englobar el procesamiento de etiquetas en componentes XML fragmentados o envueltos por hipervínculos.

## Impact

- `anonymizer/replacer.py`: Requiere actualizaciones intensivas para manipular propiedades `doc.core_properties` e iterar por nodos relacionados (o un stripping manual).
- `anonymizer/extractors/docx_extractor.py`: Debe modificarse para consolidar texto de hipervínculos unidos y buscar sobre los diccionarios de subcomponentes.
