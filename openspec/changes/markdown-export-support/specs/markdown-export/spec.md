## ADDED Requirements

### Requirement: DOCX to Markdown Conversion
The system SHALL support exporting anonymized content to Markdown format (`.md`), mapping structural elements from the source DOCX.

#### Scenario: Headers conversion
- **WHEN** a DOCX paragraph has a style mapped to a heading level (e.g., 'Heading 1')
- **THEN** it SHALL be rendered in Markdown with the corresponding number of `#` characters.

#### Scenario: Table conversion
- **WHEN** a DOCX document contains a table
- **THEN** it SHALL be rendered as a GFM (GitHub Flavored Markdown) table in the output .md file.

#### Scenario: Image exclusion
- **WHEN** exporting to Markdown
- **THEN** images SHALL be excluded from the output file to ensure a clean, text-only document.
