## Goal: Native Python Desktop GUI
The application MUST provide a native desktop interface that mirrors the CLI capabilities and allows for easy packaging into a single `.exe` file.

### Scenario: Selecting Document
- **GIVEN** the GUI is open
- **WHEN** the user clicks "Select Source" and picks a `.docx` file
- **THEN** the file path is displayed on the screen.

### Scenario: Running Detection
- **GIVEN** a file is selected
- **WHEN** the user clicks "Export entities for review (XLSX)"
- **THEN** the `detect` logic is executed and the Excel file is generated.

### Scenario: Generating Final Document
- **GIVEN** an Excel mapping file is available
- **WHEN** the user clicks "Anonymize and Create Copy"
- **THEN** a new anonymized Word file is created and a success message is shown.

### Scenario: Standalone Packaging
- **GIVEN** `pyinstaller` is configured
- **WHEN** the build command is run
- **THEN** a single `.exe` is produced that runs the GUI without needing a pre-installed Python interpreter.
