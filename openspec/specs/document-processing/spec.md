# document-processing Specification

## Purpose
TBD - created by archiving change initial-spec. Update Purpose after archive.
## Requirements
### Requirement: Word extraction and generation
System MUST read Word documents using `python-docx`, maintaining paragraph, cell, and run separation. It MUST also search across auxiliary parts (footnotes, endnotes, comments) and extract display text bound inside hyperlink XML wrappers to guarantee contiguous strings for regex entity recognition.

#### Scenario: DOCX layout preservation
- **WHEN** anonymizing a .docx file
- **THEN** generated doc output retains original text styling, tables, and layouts, except for hyperlinks which are mandatorily flattened

#### Scenario: Target extraction inside deep nodes
- **WHEN** scanning a document for names
- **THEN** the system successfully concatenates and reads entities placed inside fragmented hyperlink elements or hidden sub-containers

### Requirement: PDF extraction and generation
System MUST extract text leveraging `pdfplumber` and generate plain-text structural PDFs using `reportlab`.

#### Scenario: PDF plain text output
- **WHEN** anonymizing a .pdf file
- **THEN** generated pdf has the content with pseudonyms applied but plain text formatting without original intricate layout

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

