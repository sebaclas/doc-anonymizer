## Why

The project root is currently cluttered with a mix of documentation, assets, utility scripts, and ephemeral tool-generated files (like `opsx_out.json`). This lack of clear organization makes the project harder to navigate and maintain, and violates standard software engineering best practices for repository hygiene.

## What Changes

- **BREAKING**: Relocation of all project documentation (`MANUAL.md`, `mini_manual.md`, `mini_manual.html`, `STACK.md`, `CHANGELOG.md`, `architecture.drawio.png`) to a new `docs/` directory.
- **BREAKING**: Migration of assets (`logo.png`, `logo.ico`) to `docs/assets/`.
- **BREAKING**: Movement of packaging scripts (`build_exe.py`, `AnonymizerPro.spec`) to a new `scripts/` directory.
- Creation of a `sandbox/` directory for manual user testing and temporary files, which will be ignored by Git.
- Update of the project's `.gitignore` to support this new structure.
- Update of the application's GUI logic to correctly load assets from their new locations.

## Capabilities

### New Capabilities
<!-- - `project-hygiene`: Establishing and enforcing a standard directory structure and automated hygiene rules to keep the project root clean. -->esto ya lo agregue a las reglas globales

### Modified Capabilities
- `cli-workflow`: Update documentation and paths within the CLI tools to align with the new structure.

## Impact

- **GUI Code**: `anonymizer/gui.py` must be updated to find the logo and manual in the new `docs/` and `docs/assets/` paths.
- **Documentation Links**: `README.md` and intra-doc links must be updated.
- **Git Configuration**: `.gitignore` will be heavily modified.
- **Packaging**: The `build_exe.py` script must be adjusted to correctly package files from their new locations.
