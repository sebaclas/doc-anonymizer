## Context

Actualmente `anonymize_pdf()` en `replacer.py` usa `pdfplumber` para extraer texto y `reportlab` para generar un PDF nuevo con `SimpleDocTemplate` + `Paragraph`. Este enfoque destruye completamente el formato: fuentes originales, imágenes, tablas, colores, posiciones de texto. El PDF resultante es texto plano con Helvetica 11pt.

PyMuPDF (licencia AGPL-3.0, uso interno aceptable) ofrece la capacidad de buscar texto dentro de un PDF y aplicar "redacciones" directamente sobre el documento original, preservando todo el resto del contenido.

## Goals / Non-Goals

**Goals:**
- Implementar anonimización de PDF que preserve el formato original (fuentes, layout, tablas, imágenes).
- Usar la API de redacción de PyMuPDF: `search_for()` → `add_redact_annot()` → `apply_redactions()`.
- Mantener el motor actual como fallback ("texto plano") para casos donde PyMuPDF falle.
- Soportar los mismos modos de match (palabra/substring) que el motor DOCX.
- Respetar el orden de reemplazo (longest match first) para evitar reemplazos parciales.

**Non-Goals:**
- No soportar PDFs escaneados/imagen (OCR está fuera de scope).
- No cambiar el flujo de extracción de texto para detección NER (sigue usando pdfplumber).
- No eliminar las dependencias pdfplumber/reportlab (siguen usándose para extracción y fallback).

## Decisions

**Decision 1: Arquitectura de dos motores.**
Se crean dos funciones separadas:
- `anonymize_pdf_preserve(input, output, mapping, modes)` — PyMuPDF, preserva formato.
- `anonymize_pdf_plaintext(input, output, mapping, modes)` — reportlab, texto plano (renombrado del actual).
Un dispatcher `anonymize_pdf()` recibe un parámetro `engine` para seleccionar.
*Rationale:* Flexibilidad. PyMuPDF podría fallar en PDFs con encoding extraño o protección. El fallback garantiza que siempre se pueda generar un resultado.

**Decision 2: Estrategia de redacción con PyMuPDF.**
Para cada par (original → pseudónimo) del mapping, ordenados por longitud descendente:
1. `page.search_for(original)` encuentra todas las instancias como rectángulos.
2. `page.add_redact_annot(rect, text=pseudonym)` marca la redacción con el texto de reemplazo.
3. `page.apply_redactions()` aplica todas las redacciones de la página.
*Rationale:* La API de redacción de PyMuPDF está diseñada exactamente para este caso de uso. Maneja fuentes, colores y posicionamiento automáticamente.

**Decision 3: Manejo de fuentes.**
PyMuPDF intentará usar la fuente original del texto reemplazado. Si no es posible (fuente embebida no estándar), caerá a Helvetica. Se acepta esta limitación como tradeoff razonable.

**Decision 4: Selección de motor en las interfaces.**
- GUI: Checkbox o dropdown en el Step 2 (antes de aplicar): "Preservar formato PDF ☑" (default on).
- CLI: Flag `--pdf-engine preserve|plaintext` (default: preserve).

## Risks / Trade-offs

- [Riesgo] Textos que cruzan líneas en el PDF (ej: nombre partido entre dos lines) podrían no encontrarse con `search_for()`.
  → Mitigación: Documentar la limitación. El fallback a texto plano está disponible.
- [Riesgo] PyMuPDF agrega ~15MB al tamaño del .exe empaquetado.
  → Mitigación: Aceptable para una app de escritorio. El beneficio supera el costo.
- [Riesgo] Licencia AGPL-3.0 de PyMuPDF.
  → Mitigación: Uso interno confirmado por el usuario. No se redistribuye como producto.
- [Riesgo] El pseudónimo podría ser más largo que el original y no caber en el rect.
  → Mitigación: PyMuPDF ajusta el fontsize automáticamente o permite overflow. Evaluar en testing.
