# Tasks: Database Management Improvement

## 1. Init Logic
- [x] 1.1 Ensure `Path.home() / ".doc-anonymizer"` exists in `known_entities.py`.
- [x] 1.2 Modify `load()` to create empty JSON if file is missing.

## 2. Excel Format
- [x] 2.1 Update `mapping.save_extended_excel` to add the "Guardar en DB?" column.
- [x] 2.2 Update `mapping.load_extended_excel` (or a helper) to extract the "Guardar en DB" status.

## 3. Core Feed
- [x] 3.1 Update `anonymize_document` or `apply` logic to detect the new column.
- [x] 3.2 If "Guardar en DB" is marked, call `known_entities.add(...)`.

## 4. GUI Button
- [x] 4.1 Add a "⚙️ Configurar Base de Datos" section.
- [x] 4.2 Add button "Abrir DB Maestra (Excel)". Implement logic to export current DB to a temp file and open it.
- [x] 4.3 (Optional) Add a button to sync/import back from that Excel.
