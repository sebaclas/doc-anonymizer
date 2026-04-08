## 1. Agregar dependencia PyMuPDF

- [ ] 1.1 Agregar `PyMuPDF>=1.24` a `requirements.txt`.
- [ ] 1.2 Actualizar `STACK.md` con la nueva dependencia y su uso.

## 2. Implementar motor de redacción PyMuPDF

- [ ] 2.1 En `anonymizer/replacer.py`, crear función `anonymize_pdf_preserve(input_path, output_path, mapping, modes)` usando `fitz`.
- [ ] 2.2 Implementar búsqueda de texto por página con `page.search_for()`, ordenando keys por longitud descendente.
- [ ] 2.3 Aplicar redacciones con `add_redact_annot(rect, text=pseudo)` + `apply_redactions()`.
- [ ] 2.4 Manejar caso de PyMuPDF no disponible (fallback graceful).

## 3. Refactorizar motor existente

- [ ] 3.1 Renombrar `anonymize_pdf` actual a `anonymize_pdf_plaintext`.
- [ ] 3.2 Crear dispatcher `anonymize_pdf(input, output, mapping, modes, engine="preserve")` que seleccione el motor.

## 4. Integrar en GUI

- [ ] 4.1 Agregar checkbox/selector "Preservar formato PDF" en la interfaz (default: activado).
- [ ] 4.2 Pasar el motor seleccionado al flujo de `_apply_thread`.

## 5. Integrar en CLI

- [ ] 5.1 Agregar flag `--pdf-engine` al comando de aplicación (`preserve` | `plaintext`, default: `preserve`).
- [ ] 5.2 Pasar el motor seleccionado a `anonymize_document`.

## 6. Actualizar utilidades y build

- [ ] 6.1 Actualizar `anonymizer/utils.py` para pasar parámetro `engine` al dispatcher de PDF.
- [ ] 6.2 Actualizar `build_exe.py` / `AnonymizerPro.spec` para incluir PyMuPDF en el empaquetado.

## 7. Validación

- [ ] 7.1 Probar con un PDF con formato complejo (tablas, imágenes, fuentes especiales) — verificar que el formato se preserva.
- [ ] 7.2 Probar fallback a texto plano cuando se selecciona explícitamente.
- [ ] 7.3 Probar con PDF donde el texto del pseudónimo es más largo que el original.
- [ ] 7.4 Verificar que la detección NER (vía pdfplumber) sigue funcionando sin cambios.
