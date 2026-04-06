## 1. Documentation Alignment

- [ ] 1.1 Verify Typer CLI commands (`run`, `detect`, `apply`, `db`) map exactly to the `specs/cli-workflow` definitions
- [ ] 1.2 Verify `python-docx` logic matches requirements described in `specs/document-processing`
- [ ] 1.3 Verify `pdfplumber` and `reportlab` output matches `specs/document-processing` definition for layout loss but correct parsing

## 2. Entity Detection and Matching Modules

- [ ] 2.1 Sanity check that `spaCy`'s `xx_ent_wiki_sm` model is loaded exactly per `specs/entity-detection`
- [ ] 2.2 Review the regex definition layer to ensure it aligns with `specs/entity-detection` for CUIT, DNI, emails, and CBUs
- [ ] 2.3 Verify exact and rapidfuzz fuzzy search functionality covers `specs/entity-matching` prompt flow logic

## 3. Storage and Interactivity Validation

- [ ] 3.1 Ensure local JSON persistence path aligns with `~/.doc-anonymizer/known_entities.json` stated in architecture (`design.md`)
- [ ] 3.2 Ensure interactive dialog bindings mapped correctly to `[s/n/e]` prompt handlers.
