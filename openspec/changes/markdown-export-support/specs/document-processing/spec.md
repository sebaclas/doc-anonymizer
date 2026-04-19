# Delta: Document Processing

## EXTENDED Requirements

### Extraction of Structural Metadata
The DOCX extractor MUST capture the internal style names of paragraphs to allow for structural mapping in downstream converters.

#### Scenario: Paragraph style extraction
- **GIVEN** a DOCX paragraph with a specific style (e.g., 'Heading 1', 'Title', 'Normal')
- **WHEN** extracting content for anonymization
- **THEN** the system MUST include the style name in the intermediate data structure.
