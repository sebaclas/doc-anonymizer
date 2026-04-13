## Context

The current repository layout has many unrelated files in the root directory, including documentation, images, and ephemeral tool outputs. This design outlines the migration to a structured layout and the enforcement of agent hygiene rules.

## Goals / Non-Goals

**Goals:**
- Relocate documentation to a dedicated `docs/` hierarchy.
- Centralize visual assets in `docs/assets/`.
- Move non-core scripts (build, packaging) to a `scripts/` directory.
- Implement a `sandbox/` directory for transient testing.
- Configure all AI agent tooling to utilize `.agent/scratch/` for temporary output.
- Update internal code references to ensure the application remains functional.

**Non-Goals:**
- Deep refactoring of the internal `anonymizer` logic.
- Modification of the entity database schema or logic.

## Decisions

### Decision 1: Relative Path Resolution for Assets
**Choice**: Update `anonymizer/gui.py` to resolve assets (logo, manual) relative to the project root, targeting the new `docs/` hierarchy.
**Rationale**: Hardcoding relative paths like `../logo.png` from within a package is brittle. Using a root-relative resolution ensures portability and consistency.

### Decision 2: Standardized .gitignore Whitelisting
**Choice**: Shift to a "Deny Root by Default" strategy in `.gitignore`, explicitly allowing only standard project files (`README.md`, `pyproject.toml`, etc.) and the core directories.
**Rationale**: This prevents accidental commits of temporary test files or tool artifacts that might be generated in the root by mistake.

### Decision 3: Sandbox Directory for Interactive Use
**Choice**: Create a `sandbox/` folder at the root.
**Rationale**: Provides a consistent location for users to place test documents (`test_anon.docx`, etc.) without cluttering the root, while keeping them easily accessible for local experimentation.

### Decision 4: Agent Metadata Isolation
**Choice**: All future OpenSpec or agent workflow JSON redirections MUST use `.agent/scratch/`.
**Rationale**: Removes terminal/encoding workarounds from the visible project root, keeping the environment focused on source code.

## Risks / Trade-offs

- **[Risk] Path regression**: Moving the manual or logo might cause the GUI to crash if paths are not updated in all locations.
  - **Mitigation**: Run the GUI and verify all buttons (Manual, Logo) work before finalizing.
- **[Risk] Broken Build Script**: `build_exe.py` and `AnonymizerPro.spec` rely on specific paths for assets.
  - **Mitigation**: Update the spec file and build script to point to `docs/assets/`.
- **[Risk] User confusion**: Users accustomed to finding `mini_manual.md` in the root might get lost.
  - **Mitigation**: Update `README.md` with clear links to the new documentation location.
