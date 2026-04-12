# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-04-12

### Added
- **Document De-anonymization**: sidecar file system (`.reversal.json`) to allow precise document restoration without database dependency.
- **Automatic Pseudonym Generation**: logic to assign sequential, category-based pseudonyms (e.g., Persona1, Org1) to new entities.
- **Sidecar Reversal UI**: Action in GUI and CLI to restore original documents using sidecar files.
- **Precision Control**: Mandated manual approval for all new entity detections (NER/Regex) to prevent auto-anonymizing false positives.
- **OpenSpec Artifacts**: Internal specification system for tracking changes and tasks.

### Changed
- Improved Excel export to include document context (5 words before/after) for better vetting.
- Updated core mapping logic to handle pseudonym collisions and sequential generation.

### Fixed
- Fixed PDF processing issues related to text extraction and preservation.

## [0.2.0] - 2026-04-11

### Added
- **Excel Master Database**: Replaced JSON storage with a single source of truth in `master_database.xlsx`.
- **Automatic Migration**: Logic to convert old `known_entities.json` data to the new Excel format on first run.
- **Direct Sync**: Recognition process now loads known entities directly from the master Excel file.
- **Improved GUI**:
  - Button to open the Master Database directly in Excel.
  - Contextual help using HTML manual.
- **Diagnostics Tool**: Subagent to autopsy missing detections with precise reasons (shadowing, filters, regex failure).
- **Regression Suite**: Added standard test cases and a runner script for quality control.

### Changed
- Refactored `known_entities.py` to use `openpyxl` for all I/O operations.
- Updated `detector.py` to auto-load known entities if not provided.
- Modified custom patterns to use word boundaries (`\b`) instead of strict anchors (`^`/`$`).

### Fixed
- Fixed misleading diagnostic reports for entities caught by broad regex shadowing.
- Handled `PermissionError` when writing to Excel files locked by Microsoft Excel.

## [0.1.0] - 2026-04-01

### Added
- Initial release with DOCX/PDF support.
- NER (spaCy) and Regex engine.
- Basic GUI for document selection and mapping.
