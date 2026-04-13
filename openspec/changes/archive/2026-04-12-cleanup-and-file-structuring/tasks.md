## 1. Directory Setup & Pre-cleanup

- [x] 1.1 Create `docs/assets/`, `scripts/`, `sandbox/`, and `.agent/scratch/` directories.
- [x] 1.2 Update `.gitignore` to allow the new directory structure and ignore `sandbox/` and `.agent/scratch/` contents.
- [x] 1.3 Identify and delete legacy temporary files in the root (`opsx_*.json`, `instructions_*.json`, `status.json`, `mapping_test.xlsx`, etc.).

## 2. File Migration

- [x] 2.1 Move project documentation (`MANUAL.md`, `mini_manual.md`, `mini_manual.html`, `STACK.md`, `CHANGELOG.md`, `Notas_y_planificación.md`) to `docs/`.
- [x] 2.2 Move visual assets (`logo.png`, `logo.ico`, `architecture.drawio.png`) to `docs/assets/`.
- [x] 2.3 Move build and packaging files (`build_exe.py`, `AnonymizerPro.spec`) to `scripts/`.

## 3. Code & Configuration Updates

- [x] 3.1 Update `anonymizer/gui.py` path logic for loading the logo and opening the manuals.
- [x] 3.2 Update `README.md` with corrected links to the relocated documentation files.
- [x] 3.3 Update `scripts/build_exe.py` and `scripts/AnonymizerPro.spec` to reference assets in `docs/assets/`.
- [x] 3.4 Update any internal script references (like in `anonymizer/config.py` if applicable) to reflect the new structure.

## 4. Verification & Finalization

- [x] 4.1 Launch the GUI and verify that the logo is visible and the "Manual" button opens the correct file.
- [x] 4.2 Run a dry-run OpenSpec command and confirm redirection to `.agent/scratch/` works as intended.
- [x] 4.3 Verify `git status` reflects the clean root and correct file tracking.
