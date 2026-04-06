## ADDED Requirements

### Requirement: Document Selection Dashboard
The system SHALL provide a web-based dashboard where users can select a `.docx` or `.pdf` file to be anonymized.

#### Scenario: User selects a valid document
- **WHEN** the user drags and drops or clicks to select a `.docx` file in the UI
- **THEN** the system SHALL validate the file format and display the file name and path

### Requirement: Local Output Path Preservation
The system SHALL automatically save all generated output files (the Excel mapping and the anonymized document) in the same directory as the source file.

#### Scenario: Successful anonymization process
- **WHEN** the user confirms the detection and clicks "Process"
- **THEN** the system SHALL create the `.xlsx` mapping file and the final `.docx` in the source folder without prompting for a destination

### Requirement: Database Explorer Transition
The UI SHALL include a clear, accessible link to the known entities database.

#### Scenario: Navigating to DB
- **WHEN** the user clicks the "View Database" link
- **THEN** the system SHALL transition to a view showing all stored entities and their pseudonyms

### Requirement: Premium Visual Design
The interface SHALL follow modern design principles, including sleek typography, smooth animations, and a polished color palette (dark mode/glassmorphism).

#### Scenario: Initial Load
- **WHEN** the user opens the web application
- **THEN** the system SHALL display a visually stunning "landing" experience with clear calls to action
