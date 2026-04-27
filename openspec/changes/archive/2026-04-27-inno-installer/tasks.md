## 1. Tooling & Prerequisites

- [x] 1.1 Verify/explain Inno Setup Compiler (`ISCC`) is installed on the build machine.

## 2. Configuration & Migration

- [x] 2.1 Update `anonymizer/config.py` to use `%APPDATA%` and implement automatic legacy migration logic.
- [x] 2.2 Update PyInstaller logic or create `.spec` file to freeze the application in `--onedir` mode.
- [x] 2.3 Write the Inno Setup script (`doc-anonymizer.iss`), including the `[Code]` section for the uninstaller prompt.

## 3. Automation & Validation

- [x] 3.1 Create a single build automation script (e.g. `build_installer.bat` or `build.ps1`) to run PyInstaller followed by Inno Setup sequentially.
- [x] 3.2 Validate installing the generated `Setup_DocAnonymizer.exe`, test startup speed, and verify clean uninstallation.
