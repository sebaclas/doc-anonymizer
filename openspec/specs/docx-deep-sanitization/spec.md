# docx-deep-sanitization Specification

## Purpose
Specifies the deep sanitization workflow for DOCX files to enhance document security by purging metadata, removing hyperlink wrappers, stripping track-change history and targeting hidden nodes.

## Requirements

### Requirement: Purge document metadata
The system MUST overwrite authorship, modification history, and core properties of DOCX files to generic or empty values automatically.

#### Scenario: DOCX metadata is scrubbed
- **WHEN** anonymizing a .docx file
- **THEN** internal core_properties like `author` and `last_modified_by` are cleared

### Requirement: Flatten and strip hyperlinks
The system MUST remove hyperlink objects in the document, promoting the display text to plain runs and removing the external/internal URI relations, thus preventing URL leaks.

#### Scenario: Hyperlinks are rendered as pure text
- **WHEN** a document has an email or domain formatted as a hyperlink
- **THEN** after anonymization, the visible text persists (pseudonymized if it matched an entity) but the hyperlinked state and underlying URI data are stripped

### Requirement: Process side-parts (Footnotes, Endnotes, Comments)
The system MUST apply the entity regex mapping substitutions to text embedded inside footnotes, endnotes, and comments across all related XML parts of the document.

#### Scenario: Sensitive data in footnotes and comments is detected and anonymized
- **WHEN** an identified entity is present exclusively inside a footnote or an internal comment
- **THEN** the text is extracted for analysis, and pseudonymized in the final generated document.

### Requirement: Discard track-changes history
The system MUST simulate an "Accept All Changes" operation before anonymization by discarding all tracking XML nodes containing deleted text (`w:del`) and flattening pending inserts (`w:ins`) to ensure the final text is consolidated and no removed text survives.

#### Scenario: Review of deleted ghost text
- **WHEN** the document contains classified text that was functionally deleted by a user using Track-Changes
- **THEN** the anonymized document output permanently cleanses that text from the XML payload.
