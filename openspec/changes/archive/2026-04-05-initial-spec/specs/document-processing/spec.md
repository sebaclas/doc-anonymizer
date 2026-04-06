## ADDED Requirements

### Requirement: Word extraction and generation
System MUST read Word documents using `python-docx`, maintaining paragraph, cell, and run separation.

#### Scenario: DOCX layout preservation
- **WHEN** anonymizing a .docx file
- **THEN** generated doc output retains original text styling, tables, and layouts

### Requirement: PDF extraction and generation
System MUST extract text leveraging `pdfplumber` and generate plain-text structural PDFs using `reportlab`.

#### Scenario: PDF plain text output
- **WHEN** anonymizing a .pdf file
- **THEN** generated pdf has the content with pseudonyms applied but plain text formatting without original intricate layout
