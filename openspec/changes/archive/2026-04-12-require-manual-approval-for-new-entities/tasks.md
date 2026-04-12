## 1. GUI Implementation (Excel Mapping)

- [x] 1.1 Update `anonymizer/gui.py` to only set `accion="s"` for entities matched in the Master Database (DB hits).
- [x] 1.2 Ensure new entities (NER/Regex) have an empty `accion` string in the generated mapping rows.

## 2. CLI Implementation (Detect & Run)

- [x] 2.1 Update `anonymizer/cli.py` `detect` command to skip auto-populating the `accion` column for non-database hits.
- [x] 2.2 Update `anonymizer/review.py` (used by `anonymize run`) to default to non-approval for unknown entities.
- [x] 2.3 Verify CLI prompted reviews for unknown entities default to `n` or require explicit `s` confirmation.

## 3. Testing & Validation

- [x] 3.1 Generate a new Excel mapping file and verify `Accion` is blank for a new Regex detection (e.g., email).
- [x] 3.2 Run `anonymize run` on a test document and verify the interactive prompts for new entities default to `n`.
- [x] 3.3 Verify database hits remain auto-approved in both workflows.
