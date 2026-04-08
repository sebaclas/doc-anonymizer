## Why

El proceso actual de anonimización de PDF extrae texto con `pdfplumber` y genera un PDF completamente nuevo con `reportlab`, perdiendo todo el formato original: fuentes, tablas, imágenes, logos, colores, márgenes y estructura de página. Esto es inaceptable para documentos profesionales (contratos, informes legales, dictámenes) donde el formato es parte integral del documento.

Se necesita un mecanismo que reemplace texto directamente sobre el PDF original, preservando el layout completo.

## What Changes

- Agregar `PyMuPDF (fitz)` como nueva dependencia para redacción in-situ de PDFs.
- Crear un nuevo motor de reemplazo PDF basado en `fitz.Page.search_for()` + `add_redact_annot()` + `apply_redactions()`.
- Mantener el motor actual (`pdfplumber` + `reportlab`) como opción de fallback ("texto plano").
- Exponer la selección del motor en la GUI y CLI (default: PyMuPDF).
- Actualizar `anonymizer/replacer.py` con la nueva función `anonymize_pdf_preserve`.

## Capabilities

### New Capabilities

- `pdf-redaction`: Anonimización de PDF preservando formato original, fuentes, tablas e imágenes usando redacción in-situ.

### Modified Capabilities

- `pdf-anonymization`: El motor por defecto pasa a ser PyMuPDF. El motor anterior queda como fallback con nombre "texto plano".
- `gui-workflow`: Se agrega selector de motor PDF en la interfaz.
- `cli-workflow`: Se agrega flag `--pdf-engine` (values: `preserve` | `plaintext`, default: `preserve`).

## Impact

- `anonymizer/replacer.py`: Nueva función `anonymize_pdf_preserve()` + refactor de `anonymize_pdf()` existente.
- `anonymizer/gui.py`: Selector de motor PDF.
- `anonymizer/cli.py`: Flag `--pdf-engine`.
- `anonymizer/utils.py`: Dispatcher actualizado para pasar motor seleccionado.
- `requirements.txt`: Agregar `PyMuPDF>=1.24`.
- `STACK.md`: Documentar nueva dependencia.
- `build_exe.py` / `AnonymizerPro.spec`: Incluir PyMuPDF en el build.
