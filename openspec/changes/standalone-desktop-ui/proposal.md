# Proposal: Standalone Desktop UI (100% Python)

## Intent
Provide a user-friendly desktop application for `doc-anonymizer` that is written entirely in Python and can be packaged into a single, standalone `.exe` file without requiring complex local installations (like Node.js, browsers, or servers).

## Motivation
The current CLI tool is powerful but can be intimidating for some users. A previous "web-ui" proposal relied on FastAPI and React, which adds the overhead of a web server and a browser environment. A native Python UI (using `customtkinter`) provides:
- **Zero-Install Deployment**: Using `PyInstaller` or `Nuitka`, we can create a single exe.
- **Simplicity**: No need for REST APIs or complex frontend tooling.
- **Privacy**: No local web server listening on ports.
- **Performance**: Instant startup and lightweight footprint.

## Goals
- Add a modern desktop interface using the `customtkinter` library (Modern, "WOW" design).
- Workflow: Select DOCX/PDF -> Detect (export XLSX) -> Open XLSX -> Apply -> Final Document.
- Integrate directly with the existing `anonymizer` package.
- Support easy packaging into a single `.exe`.

## Strategy
1. **Frontend Choice**: Use `CustomTkinter` to provide a sleek, dark-themed native window.
2. **Architecture**: Implement the UI as a new module `anonymizer/gui.py` that wraps the existing CLI logic (`extract`, `detect`, `apply`).
3. **Packaging**: Include a configuration for `PyInstaller` to bundle the app and its dependencies (including the spaCy model) into one file.
4. **User Experience**: Use simple buttons and status indicators to guide the user through the multi-stage anonymization process.
