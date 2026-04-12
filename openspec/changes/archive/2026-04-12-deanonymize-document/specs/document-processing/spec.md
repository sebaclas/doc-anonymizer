## ADDED Requirements

### Requirement: Word anonymization writes reversal sidecar
The system MUST write a `.reversal.json` sidecar file alongside the anonymized DOCX output, recording the exact substitutions applied, so that the operation is reversible without accessing the master database.

#### Scenario: DOCX anonymization produces sidecar
- **WHEN** anonymizing a .docx file
- **THEN** a `<output>.reversal.json` file is created with the full list of applied substitution pairs alongside the anonymized document

### Requirement: PDF anonymization writes reversal sidecar
The system MUST write a `.reversal.json` sidecar file alongside the anonymized PDF output.

#### Scenario: PDF anonymization produces sidecar
- **WHEN** anonymizing a .pdf file
- **THEN** a `<output>.reversal.json` file is created with the full list of applied substitution pairs

### Requirement: Word de-anonymization from sidecar preserves layout
The system MUST restore a DOCX document by reading its companion sidecar file and applying the inverse substitutions using the same XML-run-level replacement strategy, preserving paragraph and run formatting.

#### Scenario: DOCX restored document retains formatting
- **WHEN** de-anonymizing a .docx file using its sidecar
- **THEN** the generated output retains original text styling, tables, and layouts; only entity text differs from the anonymized input

### Requirement: PDF de-anonymization from sidecar restores entity text
The system MUST restore a PDF document by reading its companion sidecar file and generating a new plain-structural PDF with original entity names, subject to the same formatting limitations as PDF anonymization.

#### Scenario: PDF restored with original entity names
- **WHEN** de-anonymizing a .pdf file using its sidecar
- **THEN** the generated PDF contains original entity names in place of pseudonyms, with plain text formatting
