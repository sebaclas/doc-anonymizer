## Context

Currently, `doc-anonymizer` is being packaged as an independent script, or eventually a PyInstaller standalone executable (`--onefile`). When bundled into `--onefile`, PyInstaller wraps an embedded Python interpreter, the application code, and all third-party modules (including heavy NLP dictionaries from SpaCy) into an auto-extracting archive. Every time the `.exe` is launched, it decompresses ~1GB of files into the `%TEMP%` directory, taking several seconds and frequently tripping heuristic antivirus scans.

## Goals / Non-Goals

**Goals:**
- Eliminate the startup extraction delay for end users.
- Provide a standard Windows setup process (`Setup_DocAnonymizer.exe`).
- Support shortcuts and clean uninstallation natively handled by the OS.

**Non-Goals:**
- Changing the application's core logic or GUI framework.
- Providing installers for macOS or Linux.
- Distributing Python itself globally on the machine (it continues strictly isolated to the application directory).

## Decisions

**Decision 1: Use PyInstaller `--onedir` instead of `--onefile`**
- *Rationale:* We still need to freeze the application so the user doesn't need to manually install Python and modules. By using `--onedir`, PyInstaller places the small bootloader `doc-anonymizer.exe` next to all extracted DLLs and libraries. We suffer the extraction penalty *once* (during installation), leading to instant boot times.

**Decision 2: Use Inno Setup for the Installer Shell**
- *Rationale:* Inno Setup is a mature, free, and standard compiler for Windows setup files (`.iss`). It efficiently compresses the `--onedir` folder, builds an interactive wizard, creates Desktop/Start menu shortcuts, and adds the registry keys needed for a clean uninstallation from Windows Settings.

**Decision 3: Migrate Storage from `~/.doc-anonymizer` to `%APPDATA%\doc-anonymizer`**
- *Rationale:* Following Windows standards prevents "cluttering" the user's home directory and simplifies permission management.
- *Migration strategy*: `anonymizer/config.py` will check for the existence of the old legacy folder and move files to the new location if found on first boot of the new version.

**Decision 4: Implement `CurUninstallStepChanged` in Inno Setup Script**
- *Rationale:* To satisfy the "clean uninstall" requirement, we will use Inno Setup's Pascal Scripting support to show a `MsgBox` at the end of the uninstallation process, asking to purge the AppData folder.

## Risks / Trade-offs

- **Risk:** Build process complexity slightly increases (requires installing Inno Setup Compiler locally for development). → **Mitigation**: Document the exact CLI commands or create a small `.bat` build script wrapping both tools.
- **Risk:** Windows SmartScreen warnings. Because the installer is unsigned, it might still trigger a standard "Unknown Publisher" warning on download. → **Mitigation**: Standard practice for open-source releases. The `--onedir` strategy usually reduces the more aggressive runtime Heuristic warnings, even if the SmartScreen download warning remains.
