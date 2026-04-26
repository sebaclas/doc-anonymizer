## ADDED Requirements

### Requirement: PyInstaller Directory Bundling
The build process SHALL utilize PyInstaller's `--onedir` flag (or `hatch` equivalents) to freeze the application and its massive dependencies (like SpaCy models) into an extracted directory format.

#### Scenario: Running the packaging script
- **WHEN** the user executes the project packaging command
- **THEN** an output directory is generated containing the minimal application `.exe` and all extracted supporting libraries and model files without requiring runtime extraction

### Requirement: Inno Setup Installer Generation
An Inno Setup configuration script (`.iss`) SHALL be provided to compress the generated extraction directory into a native Windows Setup executable.

#### Scenario: Compiling the installer
- **WHEN** the `.iss` script is compiled using the Inno Setup Compiler (`ISCC` or GUI)
- **THEN** a `Setup_DocAnonymizer.exe` is generated which installs the application, creates Start Menu and Desktop shortcuts, and registers an uninstaller with Windows Add/Remove Programs

### Requirement: User Data Directory (APPDATA)
The application SHALL store its configuration (`settings.json`) and database (`master_database.xlsx`) in the standard Windows `%APPDATA%\doc-anonymizer` directory to ensure compatibility with restricted environments and multi-user systems.

#### Scenario: First run on Windows
- **WHEN** the application is launched for the first time
- **THEN** it correctly creates its working directory in `%APPDATA%` without requiring Administrator privileges

### Requirement: Optional Data Purge on Uninstall
The uninstaller SHALL prompt the user to choose whether to delete their personal settings and databases or preserve them.

#### Scenario: Uninstalling the application
- **WHEN** the user uninstalls the program
- **THEN** a message box appears asking: "¿Deseas eliminar también tus configuraciones personales y la base de datos de anonimización?"
- **AND** if "YES" is selected, the `%APPDATA%\doc-anonymizer` folder is completely removed.
