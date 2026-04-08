# Tasks: Standalone Desktop UI

## 1. Environment & Dependencies
- [x] 1.1 Install `customtkinter` (pip install customtkinter).
- [x] 1.2 Update `requirements.txt`.

## 2. GUI Development
- [x] 2.1 Create the main window shell with `customtkinter`.
- [x] 2.2 Add **Step 1 Widgets**: Select file + Path preview (Supports .docx and .pdf).
- [x] 2.3 Add **Step 2 Widgets**: 
  - Option to "Start Detection" (generates revision.xlsx).
  - Option to "Load existing Excel" (Open file dialog).
- [x] 2.4 Add Status labels/previews for both Document and Excel.
- [x] 2.5 Add **Step 4 Widgets**: "Apply and Save" (must check that both a Doc and an Excel are loaded).

## 3. UI/UX Polishing
- [x] 3.1 Apply "WOW" styling (Colors, Dark Mode, Rounded corners).
- [x] 3.2 Add error popups (MB_ICONERROR) for missing files or processing failures.

## 4. Packaging (EXE)
- [x] 4.1 Install `pyinstaller` (pip install pyinstaller).
- [x] 4.2 Create a `build.py` or `.spec` file to bundle the app into a single EXE.
- [x] 4.3 Verify the EXE runs on a clean environment without Python installed.
