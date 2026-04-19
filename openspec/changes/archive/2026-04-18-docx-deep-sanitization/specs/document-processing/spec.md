## MODIFIED Requirements

### Requirement: Word extraction and generation
System MUST read Word documents using `python-docx`, maintaining paragraph, cell, and run separation. It MUST also search across auxiliary parts (footnotes, endnotes, comments) and extract display text bound inside hyperlink XML wrappers to guarantee contiguous strings for regex entity recognition.

#### Scenario: DOCX layout preservation
- **WHEN** anonymizing a .docx file
- **THEN** generated doc output retains original text styling, tables, and layouts, except for hyperlinks which are mandatorily flattened

#### Scenario: Target extraction inside deep nodes
- **WHEN** scanning a document for names
- **THEN** the system successfully concatenates and reads entities placed inside fragmented hyperlink elements or hidden sub-containers
