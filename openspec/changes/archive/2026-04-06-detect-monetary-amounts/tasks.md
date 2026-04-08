# Tasks: Implement Monetary Amount Detection

## 1. Data Model
- [x] 1.1 Add `MONEY = "MONTO"` to `EntityType` in `anonymizer/models.py`.

## 2. Detection Patterns
- [x] 2.1 Study and test regex for money in Spanish/English contexts (comma vs dot separators).
- [x] 2.2 Add `MONEY` pattern to `BUILTIN_PATTERNS` in `anonymizer/detectors/patterns.py`.
- [x] 2.3 Ensure case-insensitivity for currency words ("Pesos", "pesos").

## 3. Integration & Testing
- [x] 3.1 Verify `detect_all` returns the new entity type.
- [x] 3.2 Test with a sample document containing "$ 100", "50.00 pesos", and "USD 1.500".
- [x] 3.3 Confirm the Excel output (from `anonymize detect`) correctly shows `MONTO` as the type.
