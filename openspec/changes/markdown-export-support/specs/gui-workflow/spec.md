# Delta: GUI Workflow

## EXTENDED Requirements

### Export Format Selection
The GUI MUST allow the user to select one or more output formats for the anonymized document.

#### Scenario: Default format selection
- **WHEN** the application opens
- **THEN** 'Generar Word (.docx)' MUST be checked by default.

#### Scenario: Single or Multiple Format Selection
- **WHEN** the user selects only 'Generar Markdown (.md)'
- **THEN** only the .md file SHALL be generated.
- **WHEN** the user selects both 'Generar Word (.docx)' and 'Generar Markdown (.md)'
- **THEN** both files SHALL be generated in the output directory.

#### Scenario: Visual Layout
- **WHEN** displaying format options
- **THEN** they SHOULD be presented as checkboxes in the configuration or options panel.
