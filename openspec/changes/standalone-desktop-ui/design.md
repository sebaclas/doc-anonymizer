# Design: Native Python Desktop UI

## Overview
A single-window native desktop application for the `doc-anonymizer` project implemented with `customtkinter`. It provides a graphical interface to the same core logic used by the CLI.

## Core Components

### `anonymizer/gui.py`
The main entry point for the GUI. It will use:
- **`customtkinter`**: For a modern look and feel (dark/light mode).
- **`tkinter.filedialog`**: To pick input and output files.
- **`subprocess` / `os.startfile`**: To open the generated Excel file automatically for user review.

### Layout
- **Header**: Project logo/title.
- **Step 1 (Source)**: "Select Document" + Path Label.
- **Step 2 (Mapping Mode)**:
  - **Option A (Fresh Start)**: "Detect and Export XLSX" (runs `detect`).
  - **Option B (Manual Load)**: "Load Existing XLSX Mapping" (button to pick a file).
- **Step 3 (Review/Sync)**: Button to "Open Mapping File" (for Option A) or simply a display of the loaded path (for Option B).
- **Step 4 (Finalize)**: "Create Anonymized Copy" button. This runs `apply` using the document from Step 1 and the mapping from Step 2.

## UI Styling (WOW Factor)
- **Rounded Corners**: Using `customtkinter` built-in styles.
- **Colors**: Dark Blue/Purple theme with accent colors for "Action" buttons.
- **Animations**: Subtle button hover transitions and dynamic progress labels.

## Packaging Strategy
To satisfy the "no installations" requirement:
1. **PyInstaller**: Use a build script (`build.py`) to bundle the app.
2. **OneFile**: `--onefile` flag to produce a single `.exe`.
3. **Data Files**: 
   - Bundle `anonymizer/known_entities.json`.
   - Bundle the `spacy` model (using `--collect-data spacy`).
   - Bundle icons/images.
4. **Binary Sizes**: Expect ~100-200MB due to Python and libraries, but it requires zero setup for the end-user.
