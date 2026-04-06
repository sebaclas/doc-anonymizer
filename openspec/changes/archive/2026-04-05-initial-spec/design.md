## Context

El proyecto `doc-anonymizer` permite la anonimización de documentos Word y PDF reemplazando datos sensibles por pseudónimos consistentes. Se provee una interfaz por línea de comandos interactiva y el stack subyacente utiliza Python, Typer, python-docx, pdfplumber, spaCy (modelo xx_ent_wiki_sm), rapidfuzz y expresiones regulares. La base de documentación es el `MANUAL.md` y `STACK.md`.

## Goals / Non-Goals

**Goals:**
- Formalizar el diseño técnico actual bajo las directrices de OpenSpec.
- Documentar las responsabilidades de las librerías principales de la arquitectura del proyecto.

**Non-Goals:**
- Refactorizar código existente.
- Cambiar el comportamiento de los comandos actuales.

## Decisions

- **Framework de CLI**: Se utiliza `Typer` para la sintaxis declarativa y `Rich` para el formato e interacciones en terminal (prompts interactivos y soporte visual en la terminal).
- **Procesamiento de Documentos**: Se utiliza `python-docx` para leer/escribir preservando el formato y estructura de tablas en documentos de Word; y `pdfplumber` + `reportlab` para PDFs, aceptando el trade-off de perder el layout original en favor de una extracción de texto y tablas 100% fiable.
- **Detección de Entidades Híbrida**: Se integra tanto un modelo estadístico (NER con modelo multilingüe de `spaCy`) para nombres y lugares arbitrarios, como `re` (regex) para identificadores estandarizados (CUIT, DNI, cuentas, mails).
- **Matching y Base de Datos Local**: `rapidfuzz` se encarga de la similitud de strings (fuzzy matching) superando falsos negativos por tildes o abreviaturas, y se persiste un JSON local (`~/.doc-anonymizer/known_entities.json`) como memoria de decisiones tomadas del usuario. Adicionalmente, el formato `.xlsx` usa `openpyxl` para importación y edición manual.

## Risks / Trade-offs

- [NER Noise] El reconocimiento de entidades genera "falsos positivos" en contratos debido al capitalizado de términos legales -> Mitigación: Se provee la opción CLI `--no-ner`.
- [PDF Layout] Los archivos PDF procesados pierden la maquetación original preservando sólo el texto -> Mitigación: Uso de archivos Word (.docx) como estándar recomendado cuando se requiera preservar la maquetación y estilos.
