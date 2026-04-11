# Tasks: Diagnostic Test Suite

## Setup
- [x] Create directory `tests/regression/`
- [x] Initialize `tests/regression/cases.csv` with an empty list `[]`

## Implementation
- [x] Develop `anonymizer/diagnostics.py`
    - [x] Import `_STOPWORDS` and `_LABEL_MAP` from `anonymizer.detectors.ner`
    - [x] Import `BUILTIN_PATTERNS` from `anonymizer.detectors.patterns`
    - [x] Implement `check_filters(text)` logic
    - [x] Implement `check_shadowing(all_entities, target_span)` logic
- [x] Create `scripts/run_diagnostics.py`
    - [x] CLI argument parsing (file path, verbosity)
    - [x] Result table formatting (using `tabulate` if available or simple print)
    - [x] Logic to load and iterate over `cases.csv`

## Verification
- [x] Add 2 known "failing" cases (e.g., a word in Stopwords and an overlapping span)
- [x] Run diagnostic script and verify it correctly identifies the cause of failure
- [x] Add 1 "passing" case and verify it reports success

## Documentation
- [x] Update `MANUAL.md` with instructions on how to use the diagnostic suite to report bugs
