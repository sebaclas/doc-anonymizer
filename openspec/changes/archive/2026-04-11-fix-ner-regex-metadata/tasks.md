## 1. Core Format Updates

- [x] 1.1 Update `anonymizer/mapping.py` headers in `save_extended_excel` to `[Original, Pseudonimo, Tipo, Accion, Guardar DB, Origen, Aliases, Modo]`
- [x] 1.2 Update `anonymizer/mapping.py` row population logic in `save_extended_excel` to match new headers
- [x] 1.3 Update `anonymizer/mapping.py` loading logic in `load_extended_data` to correctly read from updated columns

## 2. GUI Enhancement

- [x] 2.1 Modify `anonymizer/gui.py` `_detection_thread` to use `ent.source.upper()` for the `origen` field
- [x] 2.2 Update `anonymizer/gui.py` `_detection_thread` to set `accion="s"` by default for entities with `source=="regex"`
- [x] 2.3 Verify `anonymizer/gui.py` dictionary keys match the new header logic

## 3. CLI Consistency

- [x] 3.1 Update `anonymizer/cli.py` `detect` command to use the new column order when exporting to Excel
- [x] 3.2 Ensure `anonymizer/cli.py` `run` command remains compatible (it uses the 2-column save by default)

## 4. Testing & Validation

- [x] 4.1 Run a detection in the GUI and verify the Excel columns are correctly ordered and "Origen" is accurate for regex
- [x] 4.2 Verify that clicking "Guardar DB" in the GUI correctly populates the Master DB without swapping Pseudonym and Type
- [x] 4.3 Verify CLI `detect` output matches the new standard format
